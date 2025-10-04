<script>
    import { onMount } from 'svelte';

    let abc = `X:1
T:The Kesh Jig
M:6/8
L:1/8
R:jig
K:G
|:G2G GBd|ege dBG|G2G GBd|ege dBA:|
|:Bdd gfg|ege dBA|Bdd gfg|age dBA:|`;

    let harmonyType = 'none';
    let melodicType = 'none';
    let lick = '';
    let tempo = 120;

    let results = null;
    let error = null;
    let loading = false;

    // Playback state
    let variationAbcs = {};
    let synthControllers = {};

    async function generateVariations() {
        console.log('[GENERATE] Starting generation...');
        console.log(`  harmony: ${harmonyType}, melodic: ${melodicType}`);

        loading = true;
        error = null;
        results = null;

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    abc,
                    harmony_type: harmonyType,
                    melodic_type: melodicType,
                    lick: lick || null,
                    validate_anglo: false
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            results = await response.json();
            console.log('[GENERATE] Results received:', results);

            // Store ABCs for playback
            variationAbcs = {
                original: results.original,
                harmony: results.harmony || '',
                melodic: results.melodic || '',
                combined: results.combined || ''
            };

            console.log('[GENERATE] Stored ABCs:', Object.keys(variationAbcs));

            // Render ABCs after DOM updates
            setTimeout(() => renderAllAbc(), 100);

        } catch (err) {
            console.error('[GENERATE ERROR]', err);
            error = err.message;
        } finally {
            loading = false;
        }
    }

    function renderAllAbc() {
        if (!window.ABCJS) {
            console.error('[RENDER] ABCJS not loaded yet');
            return;
        }

        console.log('[RENDER] Rendering all ABC notation...');

        if (results.original) {
            window.ABCJS.renderAbc('original-notation', results.original, { responsive: 'resize' });
        }

        if (results.harmony) {
            window.ABCJS.renderAbc('harmony-notation', results.harmony, { responsive: 'resize' });
        }

        if (results.melodic) {
            window.ABCJS.renderAbc('melodic-notation', results.melodic, { responsive: 'resize' });
        }

        if (results.combined) {
            window.ABCJS.renderAbc('combined-notation', results.combined, { responsive: 'resize' });
        }
    }

    function playVariation(variationType) {
        console.log(`[PLAYBACK] Playing: ${variationType}`);
        console.log(`[PLAYBACK] Available:`, Object.keys(variationAbcs));

        const abcToPlay = variationAbcs[variationType];

        if (!abcToPlay) {
            console.error(`[PLAYBACK ERROR] No ABC for ${variationType}`);
            alert(`No ${variationType} variation loaded`);
            return;
        }

        console.log(`[PLAYBACK] ABC:`, abcToPlay.substring(0, 100) + '...');

        stopAllPlayback();

        // Set tempo
        let abcWithTempo = abcToPlay;
        if (!abcWithTempo.includes('Q:')) {
            abcWithTempo = abcWithTempo.replace(/K:([^\n]+)/, `K:$1\nQ:1/4=${tempo}`);
        } else {
            abcWithTempo = abcWithTempo.replace(/Q:[^\n]+/, `Q:1/4=${tempo}`);
        }

        if (window.ABCJS.synth.supportsAudio()) {
            console.log('[PLAYBACK] Creating synth...');

            const visualObj = window.ABCJS.renderAbc('*', abcWithTempo, { visualTranspose: 0 })[0];
            const newSynth = new window.ABCJS.synth.CreateSynth();
            synthControllers[variationType] = newSynth;

            newSynth.init({
                visualObj,
                options: {
                    program: 73,
                    qpm: tempo
                }
            }).then(() => newSynth.prime())
              .then(() => {
                  console.log('[PLAYBACK] Starting...');
                  newSynth.start();
              })
              .catch(err => {
                  console.error('[PLAYBACK ERROR]', err);
                  alert('Playback failed. Check console.');
              });
        }
    }

    function stopAllPlayback() {
        Object.values(synthControllers).forEach(synth => {
            if (synth && synth.stop) {
                synth.stop();
            }
        });
    }

    onMount(() => {
        // Load ABCJS library
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/abcjs@6.4.3/dist/abcjs-basic-min.js';
        script.async = true;
        document.head.appendChild(script);
    });
</script>

<div class="container">
    <div class="section">
        <h1>Irish Tune Variation Generator</h1>
        <p>Generate harmony and melodic variations for traditional Irish tunes</p>
    </div>

    <div class="section">
        <div class="input-group">
            <label for="abc-input">ABC Notation:</label>
            <textarea id="abc-input" bind:value={abc} placeholder="Paste ABC notation here..."></textarea>
        </div>

        <div class="input-group">
            <label for="harmony-select">Harmony:</label>
            <select id="harmony-select" bind:value={harmonyType}>
                <option value="none">None</option>
                <option value="drone_pedal">Drone Pedal</option>
                <option value="parallel_thirds">Parallel Thirds</option>
                <option value="diatonic_thirds">Diatonic Thirds</option>
                <option value="open_fifths">Open Fifths</option>
            </select>
        </div>

        <div class="input-group">
            <label for="melodic-select">Melodic:</label>
            <select id="melodic-select" bind:value={melodicType}>
                <option value="none">None</option>
                <option value="neighbor">Neighbor Tones</option>
                <option value="chromatic">Chromatic Passing Tones</option>
                <option value="octave_displacement">Octave Displacement</option>
            </select>
        </div>

        <div class="input-group">
            <label for="tempo">Tempo: {tempo} BPM</label>
            <input type="range" id="tempo" bind:value={tempo} min="60" max="240" step="5">
        </div>

        <button on:click={generateVariations} disabled={loading}>
            {loading ? 'Generating...' : 'Generate Variations'}
        </button>
    </div>

    {#if error}
        <div class="section error">
            <strong>Error:</strong> {error}
        </div>
    {/if}

    {#if results}
        <div class="section">
            <h2>Original</h2>
            <div id="original-notation" class="notation"></div>
            <button class="play-button" on:click={() => playVariation('original')}>▶ Play</button>
        </div>

        {#if results.harmony}
            <div class="section variation">
                <h2>Harmony Variation</h2>
                <p class="description">{results.harmony_desc}</p>
                <div id="harmony-notation" class="notation"></div>
                <button class="play-button" on:click={() => playVariation('harmony')}>▶ Play</button>
            </div>
        {/if}

        {#if results.melodic}
            <div class="section variation">
                <h2>Melodic Variation</h2>
                <p class="description">{results.melodic_desc}</p>
                <div id="melodic-notation" class="notation"></div>
                <button class="play-button" on:click={() => playVariation('melodic')}>▶ Play</button>
            </div>
        {/if}

        {#if results.combined}
            <div class="section variation">
                <h2>Variations</h2>
                <p class="description">{results.combined_desc}</p>
                <div id="combined-notation" class="notation"></div>
                <button class="play-button" on:click={() => playVariation('combined')}>▶ Play</button>
            </div>
        {/if}
    {/if}

    <button class="stop-button" on:click={stopAllPlayback}>⏹ Stop All</button>
</div>
