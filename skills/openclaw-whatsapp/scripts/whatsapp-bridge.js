#!/usr/bin/env node
/**
 * OpenClaw WhatsApp Bridge
 * 
 * Connects WhatsApp Web to OpenClaw Gateway
 * Forwards incoming WhatsApp messages to OpenClaw and sends responses back
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
function loadEnv() {
    const envPath = path.join(__dirname, '.env');
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        envContent.split('\n').forEach(line => {
            const match = line.match(/^([^=]+)=(.*)$/);
            if (match && !process.env[match[1]]) {
                process.env[match[1]] = match[2].replace(/^["']|["']$/g, '');
            }
        });
    }
}

loadEnv();

// Configuration
const CONFIG = {
    OPENCLAW_GATEWAY_URL: process.env.OPENCLAW_GATEWAY_URL || 'http://localhost:3000',
    ALLOWED_NUMBERS: process.env.ALLOWED_NUMBERS || '',
    BLOCKED_NUMBERS: process.env.BLOCKED_NUMBERS || '',
    DEBUG: process.env.DEBUG === 'true',
    SESSION_PREFIX: process.env.SESSION_PREFIX || 'session',
    MAX_MESSAGE_LENGTH: 4000,
    REQUEST_TIMEOUT: 60000
};

// Parse allowed/blocked numbers
const allowedNumbers = CONFIG.ALLOWED_NUMBERS
    .split(',')
    .map(n => n.trim().replace(/[^0-9]/g, ''))
    .filter(n => n.length > 0);

const blockedNumbers = CONFIG.BLOCKED_NUMBERS
    .split(',')
    .map(n => n.trim().replace(/[^0-9]/g, ''))
    .filter(n => n.length > 0);

const isOpenMode = CONFIG.ALLOWED_NUMBERS === '*';

// Logger
function log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}`;
    
    if (data && CONFIG.DEBUG) {
        console.log(logEntry, data);
    } else {
        console.log(logEntry);
    }
}

// Check if number is allowed
function isAllowedNumber(number) {
    // Clean the number
    const cleanNumber = number.replace(/[^0-9]/g, '');
    
    // Check blocked list first
    if (blockedNumbers.some(blocked => cleanNumber.includes(blocked) || blocked.includes(cleanNumber))) {
        log('INFO', `Blocked number attempted contact: ${number}`);
        return false;
    }
    
    // Open mode - allow all except blocked
    if (isOpenMode) {
        return true;
    }
    
    // Check allowed list
    return allowedNumbers.some(allowed => cleanNumber.includes(allowed) || allowed.includes(cleanNumber));
}

// Forward message to OpenClaw
async function forwardToOpenClaw(message, sender) {
    try {
        const payload = {
            message: message.body,
            sender: sender,
            timestamp: new Date().toISOString(),
            platform: 'whatsapp',
            messageId: message.id?._serialized || `wa-${Date.now()}`
        };

        if (CONFIG.DEBUG) {
            log('DEBUG', 'Forwarding to OpenClaw:', payload);
        }

        const response = await axios.post(
            `${CONFIG.OPENCLAW_GATEWAY_URL}/v1/messages`,
            payload,
            {
                timeout: CONFIG.REQUEST_TIMEOUT,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (CONFIG.DEBUG) {
            log('DEBUG', 'OpenClaw response:', response.data);
        }

        return response.data?.response || response.data?.message || null;
    } catch (error) {
        log('ERROR', 'Failed to forward to OpenClaw:', error.message);
        
        if (error.response) {
            log('ERROR', 'Response status:', error.response.status);
            log('ERROR', 'Response data:', error.response.data);
        }
        
        return null;
    }
}

// Send message back to WhatsApp
async function sendResponse(client, to, text) {
    try {
        // Split long messages
        const chunks = [];
        for (let i = 0; i < text.length; i += CONFIG.MAX_MESSAGE_LENGTH) {
            chunks.push(text.slice(i, i + CONFIG.MAX_MESSAGE_LENGTH));
        }

        for (const chunk of chunks) {
            await client.sendMessage(to, chunk);
        }

        log('INFO', `Response sent to ${to} (${chunks.length} chunk(s))`);
    } catch (error) {
        log('ERROR', `Failed to send response to ${to}:`, error.message);
    }
}

// Initialize WhatsApp client
const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: path.join(__dirname, '.wwebjs_auth'),
        clientId: CONFIG.SESSION_PREFIX
    }),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-first-run',
            '--no-zygote'
        ]
    }
});

// Event: QR Code generated
client.on('qr', (qr) => {
    log('INFO', 'QR Code received! Scan with WhatsApp:');
    console.log('\n' + '='.repeat(50));
    qrcode.generate(qr, { small: true });
    console.log('='.repeat(50) + '\n');
    log('INFO', 'Waiting for QR scan...');
});

// Event: Client authenticated
client.on('authenticated', () => {
    log('INFO', 'WhatsApp authenticated successfully');
});

// Event: Client ready
client.on('ready', () => {
    log('INFO', 'WhatsApp bridge is ready!');
    log('INFO', `Gateway: ${CONFIG.OPENCLAW_GATEWAY_URL}`);
    log('INFO', `Mode: ${isOpenMode ? 'OPEN (all numbers)' : 'ALLOWLIST (' + allowedNumbers.length + ' numbers)'}`);
    log('INFO', `Debug: ${CONFIG.DEBUG ? 'ON' : 'OFF'}`);
});

// Event: Message received
client.on('message_create', async (message) => {
    // Ignore messages from self (the bot)
    if (message.fromMe) {
        return;
    }

    // Get sender info
    const contact = await message.getContact();
    const senderNumber = contact.number;
    const senderName = contact.pushname || contact.name || senderNumber;
    const chat = await message.getChat();

    if (CONFIG.DEBUG) {
        log('DEBUG', `Message from ${senderName} (${senderNumber}):`, {
            body: message.body.substring(0, 100),
            type: message.type,
            isGroup: chat.isGroup
        });
    }

    // Skip group messages (optional - remove this block to enable group support)
    if (chat.isGroup) {
        log('INFO', `Ignoring group message from ${chat.name}`);
        return;
    }

    // Check if allowed
    if (!isAllowedNumber(senderNumber)) {
        if (CONFIG.DEBUG) {
            log('DEBUG', `Message from unauthorized number: ${senderNumber}`);
        }
        return;
    }

    log('INFO', `Processing message from ${senderName} (${senderNumber})`);

    // Show typing indicator
    await chat.sendStateTyping();

    // Forward to OpenClaw
    const response = await forwardToOpenClaw(message, senderNumber);

    // Clear typing indicator
    await chat.clearState();

    // Send response back
    if (response) {
        await sendResponse(client, message.from, response);
    } else {
        await sendResponse(client, message.from, 
            "Sorry, I'm having trouble processing your message right now. Please try again later.");
    }
});

// Event: Disconnected
client.on('disconnected', (reason) => {
    log('WARN', `WhatsApp disconnected: ${reason}`);
    log('INFO', 'Attempting to reconnect in 10 seconds...');
    
    setTimeout(() => {
        client.initialize().catch(err => {
            log('ERROR', 'Failed to reconnect:', err.message);
            process.exit(1);
        });
    }, 10000);
});

// Event: Auth failure
client.on('auth_failure', (msg) => {
    log('ERROR', 'Authentication failure:', msg);
    log('INFO', 'Please delete the auth folder and scan QR again');
});

// Handle process signals
process.on('SIGTERM', async () => {
    log('INFO', 'SIGTERM received, shutting down gracefully...');
    await client.destroy();
    process.exit(0);
});

process.on('SIGINT', async () => {
    log('INFO', 'SIGINT received, shutting down gracefully...');
    await client.destroy();
    process.exit(0);
});

// Handle uncaught errors
process.on('uncaughtException', (err) => {
    log('ERROR', 'Uncaught exception:', err.message);
    if (CONFIG.DEBUG) {
        console.error(err);
    }
});

process.on('unhandledRejection', (reason, promise) => {
    log('ERROR', 'Unhandled rejection at:', promise, 'reason:', reason);
});

// Start the client
log('INFO', 'Starting OpenClaw WhatsApp Bridge...');
client.initialize().catch(err => {
    log('ERROR', 'Failed to initialize WhatsApp client:', err.message);
    process.exit(1);
});
