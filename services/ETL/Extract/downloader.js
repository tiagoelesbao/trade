const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Downloader Module: Viral ETL
 * Usa yt-dlp local para baixar vídeos de IG, TT, YT, LI.
 */
class Downloader {
    constructor(outputDir = '.aiox/tmp/downloads') {
        this.outputDir = path.resolve(outputDir);
        // Caminho para o binário local baixado
        this.binPath = path.resolve(__dirname, '..', 'bin', 'yt-dlp.exe');
        
        if (!fs.existsSync(this.outputDir)) fs.mkdirSync(this.outputDir, { recursive: true });
    }

    async probe(url) {
        const platform = url.includes('instagram') ? 'instagram' :
                        url.includes('tiktok') ? 'tiktok' :
                        url.includes('youtube') ? 'youtube' :
                        url.includes('linkedin') ? 'linkedin' : 'unknown';

        const isVideoLink = ['reel', 'video', 'watch', 'shorts'].some(p => url.includes(p)) || 
                           (platform === 'tiktok') || 
                           (platform === 'linkedin' && url.includes('activity-'));

        return {
            platform,
            type: isVideoLink ? 'video' : 'post'
        };
    }

    async downloadMetadata(url) {
        console.log(`[Downloader] Fetching metadata via HTML fallback: ${url}`);
        try {
            const response = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' } });
            const html = await response.text();
            
            // Helper to clean entities
            const clean = (str) => str ? str.replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#39;/g, "'").trim() : "";

            const title = html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["'](.*?)["']/i)?.[1] || 
                          html.match(/<title>(.*?)<\/title>/i)?.[1] || "";
            
            let description = html.match(/<meta[^>]+property=["']og:description["'][^>]+content=["'](.*?)["']/i)?.[1] || 
                              html.match(/<meta[^>]+name=["']description["'][^>]+content=["'](.*?)["']/i)?.[1] || "";
            
            const image = html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["'](.*?)["']/i)?.[1] || "";
            
            return {
                title: clean(title),
                description: clean(description),
                thumbnail: image,
                author: clean(title).split(' on ')[1] || ""
            };
        } catch (e) {
            console.error(`[Downloader] HTML metadata extraction failed: ${e.message}`);
            return { title: "", description: "", author: "" };
        }
    }

    /**
     * Download using yt-dlp with browser cookies (--cookies-from-browser chrome).
     * This is the simplest method - no manual cookie export needed.
     */
    async downloadWithBrowserCookies(url) {
        console.log(`[Downloader] Downloading via Chrome browser cookies...`);

        const bin = fs.existsSync(this.binPath) ? `"${this.binPath}"` : 'yt-dlp';
        const outputTemplate = path.join(this.outputDir, `content_${Date.now()}_%(id)s.%(ext)s`);

        // Step 1: Download video using yt-dlp with browser cookies
        console.log(`[Downloader] Running: yt-dlp --cookies-from-browser chrome ...`);
        const downloadCmd = `${bin} --cookies-from-browser chrome --no-check-certificates -f "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[ext=mp4]/best" -o "${outputTemplate}" "${url}"`;

        try {
            execSync(downloadCmd, {
                stdio: 'inherit',
                timeout: 300000 // 5 minutes
            });
        } catch (e) {
            throw new Error(`yt-dlp download with browser cookies failed: ${e.message}`);
        }

        // Step 2: Find downloaded video
        const videoExtensions = /\.(mp4|webm|mkv|mov|avi|flv)$/i;
        const files = fs.readdirSync(this.outputDir)
            .filter(f => videoExtensions.test(f))
            .map(f => ({
                name: f,
                path: path.join(this.outputDir, f),
                time: fs.statSync(path.join(this.outputDir, f)).mtimeMs,
                size: fs.statSync(path.join(this.outputDir, f)).size
            }))
            .sort((a, b) => b.time - a.time);

        if (files.length === 0) {
            throw new Error('No video file found after download');
        }

        const videoFile = files[0].path;
        const videoName = files[0].name;
        const size = files[0].size;
        console.log(`[Downloader] Video downloaded via Chrome: ${videoName} (${(size / 1024 / 1024).toFixed(1)} MB)`);

        // Step 3: Extract metadata
        let metadata = {};
        try {
            const infoCmd = `${bin} --cookies-from-browser chrome --dump-json --no-check-certificates "${url}"`;
            const jsonStr = execSync(infoCmd, {
                stdio: ['pipe', 'pipe', 'pipe'],
                timeout: 60000
            }).toString();
            const info = JSON.parse(jsonStr);
            metadata = {
                title: info.title || videoName.replace(/\.[^.]+$/, ''),
                description: info.description || "",
                author: info.uploader || info.channel || "Unknown",
                duration: info.duration,
                view_count: info.view_count,
                like_count: info.like_count,
                thumbnail: info.thumbnail
            };
        } catch (e) {
            console.warn(`[Downloader] Metadata extraction failed: ${e.message}`);
            metadata = { title: videoName.replace(/\.[^.]+$/, ''), description: "" };
        }

        return {
            videoPath: videoFile,
            images: [],
            metadata,
            status: 'success'
        };
    }

    /**
     * Usa o bot Python do YouTube para download mais confiável
     * @param {string} url - URL do vídeo
     * @param {string|null} cookiesPath - Caminho dos cookies (null = sem cookies)
     */
    async downloadWithPythonBot(url, cookiesPath = null, maxDuration = 600) {
        const botDir = 'C:\\Users\\Pichau\\Desktop\\Sistemas\\SaAS\\Bot_youtube';
        const cookiesFile = path.join(botDir, 'youtube.com_cookies.txt');
        const ffmpegPath = path.join(botDir, 'ffmpeg-7.1.1-essentials_build', 'bin');

        if (!fs.existsSync(path.join(botDir, 'boyt_yt.py'))) {
            throw new Error('Python bot not found');
        }

        console.log(`[Downloader] Using Python YouTube bot...`);

        // Create a temp Python script that downloads a single video
        const tempScript = path.join(this.outputDir, `temp_dl_${Date.now()}.py`);
        const outputDir = this.outputDir;

        const effectiveCookies = cookiesPath || (fs.existsSync(cookiesFile) ? cookiesFile : null);

        const pythonScript = `
import sys
import os
import json
sys.path.insert(0, '${botDir.replace(/\\/g, '/')}')
os.environ['PATH'] = r'${ffmpegPath.replace(/\\/g, '/')};' + os.environ.get('PATH', '')

from boyt_yt import check_ffmpeg_installed
import yt_dlp

url = '${url}'
output = r'${outputDir}'
cookies = r'${effectiveCookies.replace(/\\/g, '/')}' if ${effectiveCookies ? 'True' : 'False'} and os.path.isfile(r'${effectiveCookies.replace(/\\/g, '/')}') else None
ffmpeg = check_ffmpeg_installed()

print(f"[Python Bot] Downloading: {url}")
print(f"[Python Bot] FFmpeg: {ffmpeg}, Cookies: {bool(cookies)}")

# Use lower quality for faster processing (480p max)
ydl_opts = {
    'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[ext=mp4]/best',
    'outtmpl': os.path.join(output, '%(title)s.%(ext)s'),
    'quiet': False,
    'no_warnings': False,
    'no_check_certificate': True,
    'geo_bypass': True,
    'retries': 3,
    'fragment_retries': 3,
    'merge_output_format': 'mp4' if ffmpeg else None,
    # JS runtime for solving YouTube n-challenges (requires yt-dlp >= 2026.3 + EJS 0.8.0)
    'js_runtimes': {'node': {}},
    'remote_components': ['ejs:github'],
}

if cookies:
    ydl_opts['cookiefile'] = cookies

print(f"[Python Bot] Quality: 480p max (optimized for benchmark)")
print(f"[Python Bot] JS Runtime: Node.js + EJS remote component")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is None:
            print(f"[Python Bot] Error: Could not get video info")
            sys.exit(1)
        downloaded_file = ydl.prepare_filename(info)
        title = info.get('title', 'unknown')
        duration = info.get('duration', 0)
        format_count = len(info.get('formats', []))
        print(f"[Python Bot] Result: success")
        print(f"[Python Bot] File: {downloaded_file}")
        print(f"[Python Bot] Title: {title}")
        print(f"[Python Bot] Duration: {duration}s")
        print(f"[Python Bot] Formats: {format_count}")
        # Write info JSON for metadata extraction
        info_json = json.dumps({
            'title': title,
            'description': info.get('description', ''),
            'uploader': info.get('uploader', 'Unknown'),
            'channel': info.get('channel', ''),
            'duration': duration,
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'thumbnail': info.get('thumbnail')
        })
        info_file = downloaded_file + '.info.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_json)
        print(f"[Python Bot] Info JSON written to: {info_file}")
except Exception as e:
    print(f"[Python Bot] Error: {str(e)}")
    sys.exit(1)
`;

        fs.writeFileSync(tempScript, pythonScript);

        try {
            const { execSync } = require('child_process');
            console.log(`[Downloader] Running Python bot script...`);
            execSync(`python "${tempScript}"`, {
                stdio: 'inherit',
                timeout: 300000 // 5 minutes
            });

            // Find downloaded video file
            const videoExtensions = /\.(mp4|webm|mkv|mov|avi|flv)$/i;
            const files = fs.readdirSync(this.outputDir)
                .filter(f => videoExtensions.test(f))
                .map(f => ({
                    name: f,
                    path: path.join(this.outputDir, f),
                    time: fs.statSync(path.join(this.outputDir, f)).mtimeMs,
                    size: fs.statSync(path.join(this.outputDir, f)).size
                }))
                .sort((a, b) => b.time - a.time);

            // Find info JSON file
            const infoJsonFile = files.length > 0 
                ? files[0].path + '.info.json' 
                : null;

            if (files.length > 0) {
                const videoFile = files[0].path;
                const size = files[0].size;
                const videoName = files[0].name;
                console.log(`[Downloader] Video downloaded: ${videoName} (${(size / 1024 / 1024).toFixed(1)} MB)`);

                // Extract metadata from info JSON or yt-dlp
                let metadata = {};
                if (infoJsonFile && fs.existsSync(infoJsonFile)) {
                    try {
                        const infoData = JSON.parse(fs.readFileSync(infoJsonFile, 'utf8'));
                        metadata = {
                            title: infoData.title || videoName.replace(/\.[^.]+$/, ''),
                            description: infoData.description || "",
                            author: infoData.uploader || infoData.channel || "Unknown",
                            duration: infoData.duration,
                            view_count: infoData.view_count,
                            like_count: infoData.like_count,
                            thumbnail: infoData.thumbnail
                        };
                    } catch (e) {
                        console.warn(`[Downloader] Failed to read info JSON: ${e.message}`);
                        metadata = { title: videoName.replace(/\.[^.]+$/, ''), description: "" };
                    }
                } else {
                    // Fallback to yt-dlp --dump-json
                    try {
                        const bin = fs.existsSync(this.binPath) ? `"${this.binPath}"` : 'yt-dlp';
                        const cookiesFlag = fs.existsSync(cookiesFile) ? `--cookies "${cookiesFile}"` : '';
                        const jsonStr = execSync(`${bin} --dump-json --no-check-certificates ${cookiesFlag} "${url}"`, {
                            stdio: ['pipe', 'pipe', 'pipe'],
                            timeout: 60000
                        }).toString();
                        const info = JSON.parse(jsonStr);
                        metadata = {
                            title: info.title || videoName.replace(/\.[^.]+$/, ''),
                            description: info.description || "",
                            author: info.uploader || info.channel || "Unknown",
                            duration: info.duration,
                            view_count: info.view_count,
                            like_count: info.like_count,
                            thumbnail: info.thumbnail
                        };
                    } catch (e) {
                        metadata = { title: videoName.replace(/\.[^.]+$/, ''), description: "" };
                    }
                }

                return {
                    videoPath: videoFile,
                    images: [],
                    metadata,
                    status: 'success'
                };
            }

            throw new Error('No video file found after Python bot execution');
        } finally {
            // Cleanup temp script
            try { fs.unlinkSync(tempScript); } catch (_) {}
        }
    }

    async download(url) {
        const { platform, type } = await this.probe(url);

        // Segmentação: Se for Post de Instagram (/p/) e não detectado como vídeo
        if (platform === 'instagram' && type === 'post' && url.includes('/p/')) {
            console.log(`[Downloader] Specialized Instagram Post/Carousel detected: ${url}`);
            try {
                const CarouselScraper = require('./scrapers/instagram-carousel');
                const scraper = new CarouselScraper();
                await scraper.init();
                const scrapedData = await scraper.extract(url, this.outputDir);
                await scraper.close();

                if (scrapedData.status === 'success' || (scrapedData.images && scrapedData.images.length > 0)) {
                    return {
                        videoPath: null,
                        images: scrapedData.images || [],
                        metadata: {
                            title: scrapedData.title || 'Instagram Post',
                            description: scrapedData.description || "",
                            author: scrapedData.author || "Unknown",
                            thumbnail: scrapedData.images[0] || null,
                            raw_meta: scrapedData.raw_meta || ""
                        },
                        status: 'success'
                    };
                }
            } catch (scErr) {
                console.error(`[Downloader] InstagramCarouselScraper failed:`, scErr);
            }
        }

        // Segmentação: LinkedIn posts com sessão autenticada
        if (platform === 'linkedin' && (url.includes('/feed/update/') || url.includes('/posts/'))) {
            console.log(`[Downloader] Specialized LinkedIn Post detected: ${url}`);
            try {
                const LinkedInScraper = require('./scrapers/linkedin');
                const scraper = new LinkedInScraper();
                await scraper.init();
                const scrapedData = await scraper.extract(url);
                await scraper.close();

                if (scrapedData.status === 'success' || scrapedData.description) {
                    return {
                        videoPath: null,
                        images: [],
                        metadata: {
                            title: scrapedData.title || 'LinkedIn Post',
                            description: scrapedData.description || "",
                            author: scrapedData.author || "Unknown",
                            thumbnail: scrapedData.imageUrl || null,
                            like_count: scrapedData.likes || null,
                            comment_count: scrapedData.comments || null
                        },
                        status: scrapedData.status || 'metadata_only'
                    };
                }
            } catch (liErr) {
                console.error(`[Downloader] LinkedInScraper failed:`, liErr.message);
            }
        }

        // Fluxo de Vídeo — tenta yt-dlp local OU Python bot do YouTube
        const filenameTemplate = `content_${Date.now()}_%(id)s_%(n)s.%(ext)s`;
        const outputPath = path.join(this.outputDir, filenameTemplate);

        console.log(`[Downloader] Attempting extraction via yt-dlp: ${url}`);

        try {
            // Check for cookies file for authentication
            let cookiesFlag = '';
            const localCookies = path.resolve(__dirname, '..', 'auth', 'cookies.txt');
            const botCookies = 'C:\\Users\\Pichau\\Desktop\\Sistemas\\SaAS\\Bot_youtube\\youtube.com_cookies.txt';
            const botCookiesJson = 'C:\\Users\\Pichau\\Desktop\\Sistemas\\SaAS\\Bot_youtube\\exported-cookies.json';

            if (fs.existsSync(botCookies)) {
                cookiesFlag = `--cookies "${botCookies}"`;
                console.log(`[Downloader] Using cookies from Bot_youtube: ${botCookies}`);
            } else if (fs.existsSync(localCookies)) {
                cookiesFlag = `--cookies "${localCookies}"`;
            }

            // For YouTube, try browser cookies first (simplest method)
            if (platform === 'youtube') {
                console.log(`[Downloader] YouTube detected — trying browser cookies first...`);
                try {
                    const result = await this.downloadWithBrowserCookies(url);
                    if (result && result.status === 'success') {
                        return result;
                    }
                } catch (browserErr) {
                    console.log(`[Downloader] Browser cookies failed: ${browserErr.message}`);
                }

                // Fallback to Python bot with file cookies
                console.log(`[Downloader] Trying Python bot as fallback...`);
                try {
                    const result = await this.downloadWithPythonBot(url, null);
                    if (result && result.status === 'success') {
                        return result;
                    }
                } catch (pyErr) {
                    console.log(`[Downloader] Python bot also failed: ${pyErr.message}`);
                }
            }

            const bin = fs.existsSync(this.binPath) ? `"${this.binPath}"` : 'yt-dlp';

            // Important: we try to force mp4 for better compatibility, but fallback to any format if needed.
            const cmd = `${bin} --write-info-json --no-check-certificates ${cookiesFlag} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "${outputPath}" "${url}"`;
            
            try {
                execSync(cmd, { stdio: 'pipe' });
            } catch (dlError) {
                console.warn(`[Downloader] yt-dlp failed for ${url}. Trying without forced mp4...`);
                // Retry without forcing mp4 if it failed (some old videos might not have it)
                try {
                    const fallbackCmd = `${bin} --write-info-json --no-check-certificates ${cookiesFlag} -o "${outputPath}" "${url}"`;
                    execSync(fallbackCmd, { stdio: 'pipe' });
                } catch (retryError) {
                    console.warn(`[Downloader] yt-dlp final failure for ${url}.`);
                    
                    // Try Scraper Fallback if it's Instagram
                    if (platform === 'instagram') {
                        console.log(`[Downloader] Trying InstagramScraper fallback after yt-dlp failure...`);
                        try {
                            const InstagramScraper = require('./scrapers/instagram');
                            const scraper = new InstagramScraper();
                            await scraper.init();
                            const scrapedData = await scraper.extract(url, this.outputDir);
                            await scraper.close();

                            if (scrapedData.status === 'success' || (scrapedData.images && scrapedData.images.length > 0)) {
                                return {
                                    videoPath: null,
                                    images: scrapedData.images || [],
                                    metadata: {
                                        title: scrapedData.title,
                                        description: scrapedData.description,
                                        author: scrapedData.author,
                                        thumbnail: scrapedData.imageUrl
                                    },
                                    status: scrapedData.images.length > 0 ? 'success' : 'metadata_only'
                                };
                            }
                        } catch (scErr) {
                            console.error(`[Downloader] InstagramScraper fallback failed:`, scErr.message);
                        }
                    }

                    console.log(`[Downloader] Falling back to metadata only HTML.`);
                    const metadata = await this.downloadMetadata(url);
                    return { videoPath: null, images: [], metadata, status: 'metadata_only' };
                }
            }

            // Collect all files generated by this download run
            const files = fs.readdirSync(this.outputDir)
                           .filter(f => f.startsWith(`content_${Date.now().toString().substring(0, 8)}`));
            
            const infoJsonFile = files.find(f => f.endsWith('.info.json'));
            const videoFile = files.find(f => f.match(/\.(mp4|webm|mkv|mov|avi|flv)$/i));
            const imageFiles = files.filter(f => f.match(/\.(jpg|jpeg|png|webp)$/i));

            let metadata = {};
            if (infoJsonFile) {
                try {
                    const fullPath = path.join(this.outputDir, infoJsonFile);
                    const rawData = fs.readFileSync(fullPath, 'utf8');
                    const fullInfo = JSON.parse(rawData);
                    metadata = {
                        title: fullInfo.title || "Unknown Title",
                        description: fullInfo.description || "",
                        author: fullInfo.uploader || fullInfo.channel || "Unknown",
                        duration: fullInfo.duration,
                        view_count: fullInfo.view_count,
                        like_count: fullInfo.like_count,
                        thumbnail: fullInfo.thumbnail
                    };
                    fs.unlinkSync(fullPath);
                } catch (e) {
                    console.error("[Downloader] Failed to parse info JSON", e.message);
                }
            }

            if (videoFile || imageFiles.length > 0) {
                return { 
                    videoPath: videoFile ? path.join(this.outputDir, videoFile) : null, 
                    images: imageFiles.map(img => path.join(this.outputDir, img)),
                    metadata, 
                    status: 'success' 
                };
            }
            
            const metadataFallback = await this.downloadMetadata(url);
            return { videoPath: null, images: [], metadata: metadataFallback, status: 'metadata_only' };
        } catch (error) {
            console.error(`[Downloader] Error in download process:`, error.message);
            throw error;
        }
    }

    cleanup(filePath) {
        if (filePath && fs.existsSync(filePath)) {
            try { fs.unlinkSync(filePath); } catch(e) {}
        }
    }
}

module.exports = Downloader;
