/**
 * Shared Playback Module for Irish Tune Variation Generator
 * Handles ABCJS audio playback with comprehensive logging
 */

// Playback state
let synthControllers = {};

/**
 * Play variation with ABCJS synth
 * @param {string} variationType - Key for variation (e.g., 'original', 'melodic')
 * @param {object} variationAbcs - Object mapping variation types to ABC strings
 * @param {number} tempo - Tempo in BPM
 */
export function playVariation(variationType, variationAbcs, tempo) {
    console.log(`[PLAYBACK] Playing variation type: ${variationType}`);
    console.log(`[PLAYBACK] Available variations:`, Object.keys(variationAbcs));

    const abc = variationAbcs[variationType];
    console.log(`[PLAYBACK] ABC for ${variationType}:`, abc ? abc.substring(0, 100) + '...' : 'NOT FOUND');

    if (!abc) {
        console.error(`[PLAYBACK ERROR] No ABC found for variation: ${variationType}`);
        alert(`No ${variationType} variation loaded`);
        return;
    }

    console.log(`[PLAYBACK] Tempo: ${tempo} BPM`);

    // Stop all currently playing music
    stopAllPlayback();

    // Set tempo in ABC notation
    let abcWithTempo = abc;
    if (!abcWithTempo.includes('Q:')) {
        abcWithTempo = abcWithTempo.replace(/K:([^\n]+)/, `K:$1\nQ:1/4=${tempo}`);
    } else {
        abcWithTempo = abcWithTempo.replace(/Q:[^\n]+/, `Q:1/4=${tempo}`);
    }
    console.log(`[PLAYBACK] ABC with tempo set:`, abcWithTempo.substring(0, 150) + '...');

    // Create synth and play
    if (ABCJS.synth.supportsAudio()) {
        console.log(`[PLAYBACK] Audio supported, creating synth...`);

        // Parse ABC for audio only (don't re-render visuals)
        const visualObj = ABCJS.renderAbc('*', abcWithTempo, {
            visualTranspose: 0
        })[0];
        console.log(`[PLAYBACK] Visual object created:`, visualObj);

        // Always create a NEW synth (can't reuse them)
        const newSynth = new ABCJS.synth.CreateSynth();
        synthControllers[variationType] = newSynth;
        console.log(`[PLAYBACK] New synth created for ${variationType}`);

        newSynth.init({
            visualObj: visualObj,
            options: {
                program: 73, // Flute sound
                qpm: tempo
            }
        }).then(() => {
            console.log(`[PLAYBACK] Synth initialized, priming...`);
            return newSynth.prime();
        }).then(() => {
            console.log(`[PLAYBACK] Synth primed, starting playback...`);
            newSynth.start();
            console.log(`[PLAYBACK] Playback started successfully`);
        }).catch(error => {
            console.error('[PLAYBACK ERROR] Playback failed:', error);
            alert('Playback failed. Check console for details.');
        });
    } else {
        console.error('[PLAYBACK ERROR] Audio not supported in browser');
        alert('Audio not supported in this browser');
    }
}

/**
 * Stop all currently playing synths
 */
export function stopAllPlayback() {
    console.log('[PLAYBACK] Stopping all playback...');
    Object.values(synthControllers).forEach(synth => {
        if (synth && synth.stop) {
            synth.stop();
        }
    });
    console.log('[PLAYBACK] All playback stopped');
}

/**
 * Render ABC notation to a DOM element
 * @param {string} elementId - ID of DOM element to render into
 * @param {string} abc - ABC notation string
 */
export function renderAbc(elementId, abc, options = {}) {
    console.log(`[RENDER] Rendering ABC to #${elementId}`);
    if (!abc) {
        console.error(`[RENDER ERROR] No ABC provided for #${elementId}`);
        return;
    }

    const defaultOptions = { responsive: 'resize' };
    const mergedOptions = { ...defaultOptions, ...options };

    ABCJS.renderAbc(elementId, abc, mergedOptions);
    console.log(`[RENDER] Successfully rendered to #${elementId}`);
}

export function renderAbcWrapped(elementId, abc) {
    console.log(`[RENDER] Rendering wrapped ABC to #${elementId}`);
    const element = document.getElementById(elementId);
    if (!element) {
        console.error(`[RENDER ERROR] Element #${elementId} not found`);
        return;
    }

    const containerWidth = element.parentElement?.offsetWidth || 800;

    renderAbc(elementId, abc, {
        staffwidth: containerWidth - 40,
        wrap: {
            minSpacing: 1.5,
            maxSpacing: 2.5,
            preferredMeasuresPerLine: 4
        }
    });
}
