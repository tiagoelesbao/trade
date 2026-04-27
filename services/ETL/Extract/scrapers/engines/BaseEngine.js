const fs = require('fs');
const path = require('path');

class BaseEngine {
    constructor(parent) {
        this.parent = parent; // Referência ao orquestrador Chief
        this.now = parent.now;
        this.lookbackLimit = parent.lookbackLimit;
    }

    logDiagnostic(msg) {
        this.parent.logDiagnostic(msg);
    }

    async applyStealth(context) {
        await context.addInitScript(() => {
            delete Object.getPrototypeOf(navigator).webdriver;
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {
                get: () => ['pt-BR', 'pt', 'en-US', 'en'],
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        });
    }

    parseSmartDate(dateText) {
        if (!dateText) return null;
        let text = dateText.toLowerCase()
            .replace(/^[^\w\d\s]+/, '') 
            .replace(/há/g, '')
            .replace(/atrás/g, '')
            .replace(/•/g, '')
            .trim();

        const relativeMatch = text.match(/^(\d+)\s*(h|d|dia|sem|m|min|s|w|y|ano)/);
        
        if (relativeMatch) {
            const num = parseInt(relativeMatch[1]);
            const unit = relativeMatch[2];
            let d = new Date();
            if (unit.startsWith('h')) d.setHours(d.getHours() - num);
            else if (unit.startsWith('d') || unit.startsWith('dia')) d.setDate(d.getDate() - num);
            else if (unit === 'm' || unit.startsWith('min')) d.setMinutes(d.getMinutes() - num); // Correção: 'm' sozinho era ambíguo
            else if (unit.startsWith('s')) d.setSeconds(d.getSeconds() - (num * 10));
            else if (unit.startsWith('w') || unit.startsWith('sem')) d.setDate(d.getDate() - (num * 7));
            else if (unit.startsWith('y') || unit.startsWith('ano')) d.setFullYear(d.getFullYear() - num);
            return d;
        }

        const absoluteMatch = text.match(/^(\d{4}) (\d{1,2}) (\d{1,2})/);
        if (absoluteMatch) {
            return new Date(parseInt(absoluteMatch[1]), parseInt(absoluteMatch[2]) - 1, parseInt(absoluteMatch[3]));
        }

        return null;
    }

    parseViralMetric(text) {
        if (!text) return 0;
        let clean = text.toString().toLowerCase().trim();
        const match = clean.match(/([\d\.,]+)\s*([kmb]|mil|mi)?/);
        if (!match) return 0;
        
        let numStr = match[1];
        let suffix = match[2];
        
        if (suffix === 'mil') suffix = 'k';
        if (suffix === 'mi') suffix = 'm';
        
        if (numStr.includes('.') && numStr.includes(',')) {
            if (numStr.lastIndexOf('.') < numStr.lastIndexOf(',')) {
                numStr = numStr.replace(/\./g, '').replace(',', '.');
            } else {
                numStr = numStr.replace(/,/g, '');
            }
        } else if (numStr.includes(',')) {
            if (suffix) numStr = numStr.replace(',', '.');
            else {
                const parts = numStr.split(',');
                if (parts[parts.length - 1].length === 3) numStr = numStr.replace(/,/g, '');
                else numStr = numStr.replace(',', '.');
            }
        } else if (numStr.includes('.')) {
            if (!suffix) {
                const parts = numStr.split('.');
                if (parts[parts.length - 1].length === 3 || parts.length > 2) numStr = numStr.replace(/\./g, '');
            }
        }

        let num = parseFloat(numStr);
        if (suffix === 'k') num *= 1000;
        else if (suffix === 'm') num *= 1000000;
        else if (suffix === 'b') num *= 1000000000;
        
        return isNaN(num) ? 0 : Math.round(num);
    }

    calculateScore(metrics) {
        return (metrics.views * 0.1) + (metrics.likes * 1) + (metrics.comments * 5);
    }

    isWithinWindow(date) {
        if (!date) return false;
        return date >= this.lookbackLimit && date <= this.now;
    }
}

module.exports = BaseEngine;
