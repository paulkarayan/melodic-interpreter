/**
 * Shared API Module for Irish Tune Variation Generator
 * Handles all backend API calls with logging
 */

/**
 * Generate melodic variations
 * @param {string} abc - ABC notation
 * @param {string} melodicType - Type of melodic variation
 * @param {string} lick - Optional target lick pattern
 */
export async function generateMelodicVariation(abc, melodicType, lick = null) {
    console.log('[API] Generating melodic variation...');
    console.log(`  - melodic_type: ${melodicType}`);
    console.log(`  - lick: ${lick || 'none'}`);

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            abc: abc,
            harmony_type: 'none',
            melodic_type: melodicType,
            lick: lick,
            validate_anglo: false
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Response received:', data);
    return data;
}

/**
 * Generate harmony variations
 * @param {string} abc - ABC notation
 * @param {string} harmonyType - Type of harmony variation
 */
export async function generateHarmonyVariation(abc, harmonyType) {
    console.log('[API] Generating harmony variation...');
    console.log(`  - harmony_type: ${harmonyType}`);

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            abc: abc,
            harmony_type: harmonyType,
            melodic_type: 'none',
            lick: null,
            validate_anglo: false
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Response received:', data);
    return data;
}

/**
 * Generate combined variations
 * @param {string} abc - ABC notation
 * @param {string} harmonyType - Type of harmony variation
 * @param {string} melodicType - Type of melodic variation
 * @param {string} lick - Optional target lick pattern
 */
export async function generateCombinedVariation(abc, harmonyType, melodicType, lick = null) {
    console.log('[API] Generating combined variation...');
    console.log(`  - harmony_type: ${harmonyType}`);
    console.log(`  - melodic_type: ${melodicType}`);

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            abc: abc,
            harmony_type: harmonyType,
            melodic_type: melodicType,
            lick: lick,
            validate_anglo: false
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Response received:', data);
    return data;
}

/**
 * Analyze session variations
 * @param {string} url - The Session URL
 */
export async function analyzeSession(url) {
    console.log('[API] Analyzing session:', url);

    const response = await fetch('/analyze-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Session analysis received:', data);
    return data;
}

/**
 * Generate style transformations
 * @param {string} abc - ABC notation
 * @param {array} styles - Array of style names
 */
export async function generateStyleTransformations(abc, styles) {
    console.log('[API] Generating style transformations...');
    console.log(`  - styles: ${styles.join(', ')}`);

    const response = await fetch('/transform-styles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            abc: abc,
            styles: styles
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Style transformations received:', data);
    return data;
}

/**
 * Feeling lucky - random combinations
 * @param {string} abc - ABC notation
 */
export async function feelingLucky(abc) {
    console.log('[API] Generating feeling lucky variations...');

    const response = await fetch('/feeling-lucky', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            abc: abc,
            validate_anglo: false
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Feeling lucky variations received:', data);
    return data;
}
