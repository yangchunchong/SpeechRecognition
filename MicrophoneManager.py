<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>语音识别系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .main-content {
            padding: 40px;
        }
        
        .tab-container {
            display: flex;
            border-bottom: 2px solid #eee;
            margin-bottom: 30px;
        }
        
        .tab {
            padding: 15px 30px;
            background: none;
            border: none;
            font-size: 16px;
            cursor: pointer;
            position: relative;
            color: #666;
            transition: all 0.3s;
        }
        
        .tab.active {
            color: #667eea;
        }
        
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 3px;
            background: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        select, button {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
            letter-spacing: 1px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .file-upload {
            border: 2px dashed #e0e0e0;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .file-upload:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .file-upload input {
            display: none;
        }
        
        .file-upload i {
            font-size: 48px;
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .recorder {
            text-align: center;
        }
        
        .record-btn {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 24px;
            margin: 20px 0;
            transition: all 0.3s;
        }
        
        .record-btn.recording {
            background: #ff4757;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .result-container {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .result-text {
            font-size: 18px;
            line-height: 1.6;
            color: #333;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .history-link {
            text-align: center;
            margin-top: 20px;
        }
        
        .history-link a {
            color: #667eea;
            text-decoration: none;
        }
        
        .history-link a:hover {
            text-decoration: underline;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>语音识别系统</h1>
            <p class="subtitle">支持多种语音识别引擎，实时将语音转换为文字</p>
        </header>
        
        <div class="main-content">
            <div class="tab-container">
                <button class="tab active" onclick="switchTab('file-tab')">
                    <i class="fas fa-file-upload"></i> 文件上传
                </button>
                <button class="tab" onclick="switchTab('record-tab')">
                    <i class="fas fa-microphone"></i> 实时录音
                </button>
            </div>
            
            <!-- 文件上传标签页 -->
            <div id="file-tab" class="tab-content active">
                <div class="form-group">
                    <label>选择识别引擎</label>
                    <select id="engine">
                        <option value="google">Google Speech Recognition</option>
                        <option value="whisper">OpenAI Whisper</option>
                        <option value="vosk">Vosk (离线)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>选择语言</label>
                    <select id="language">
                        <!-- 语言选项将通过JavaScript动态加载 -->
                    </select>
                </div>
                
                <div class="form-group">
                    <label>上传音频文件</label>
                    <div class="file-upload" id="drop-area">
                        <i class="fas fa-cloud-upload-alt"></i>
                        <p>拖放文件到这里，或点击选择文件</p>
                        <p style="color: #666; font-size: 14px; margin-top: 10px;">
                            支持格式: WAV, MP3, M4A, OGG, FLAC
                        </p>
                        <input type="file" id="file-input" accept="audio/*">
                    </div>
                </div>
                
                <button id="upload-btn">
                    <i class="fas fa-paper-plane"></i> 开始识别
                </button>
            </div>
            
            <!-- 实时录音标签页 -->
            <div id="record-tab" class="tab-content">
                <div class="form-group">
                    <label>选择识别引擎</label>
                    <select id="record-engine">
                        <option value="google">Google Speech Recognition</option>
                        <option value="whisper">OpenAI Whisper</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>选择语言</label>
                    <select id="record-language">
                        <!-- 语言选项将通过JavaScript动态加载 -->
                    </select>
                </div>
                
                <div class="recorder">
                    <p>点击下方按钮开始录音</p>
                    <button class="record-btn" id="record-btn">
                        <i class="fas fa-microphone"></i>
                    </button>
                    <p id="timer">00:00</p>
                    <p id="status">准备录音</p>
                </div>
            </div>
            
            <!-- 结果展示 -->
            <div id="result-section" style="display: none;">
                <h3>识别结果</h3>
                <div class="result-container">
                    <div class="result-text" id="result-text"></div>
                </div>
                <button onclick="copyResult()" style="margin-top: 15px;">
                    <i class="fas fa-copy"></i> 复制结果
                </button>
            </div>
            
            <!-- 加载中 -->
            <div id="loading" class="loading" style="display: none;">
                <div class="spinner"></div>
                <p>正在识别中，请稍候...</p>
            </div>
            
            <div class="history-link">
                <a href="/history"><i class="fas fa-history"></i> 查看历史记录</a>
            </div>
        </div>
    </div>

    <script>
        // 当前激活的标签页
        let activeTab = 'file-tab';
        
        // 录音相关变量
        let mediaRecorder = null;
        let audioChunks = [];
        let isRecording = false;
        let timerInterval = null;
        let seconds = 0;
        
        // 切换标签页
        function switchTab(tabId) {
            // 隐藏当前标签页
            document.querySelector(`#${activeTab}`).classList.remove('active');
            document.querySelector(`button[onclick="switchTab('${activeTab}')"]`).classList.remove('active');
            
            // 显示新标签页
            document.querySelector(`#${tabId}`).classList.add('active');
            document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');
            
            activeTab = tabId;
            
            // 如果是录音标签页，停止可能正在进行的录音
            if (tabId !== 'record-tab' && isRecording) {
                stopRecording();
            }
        }
        
        // 加载语言列表
        async function loadLanguages() {
            try {
                const response = await fetch('/api/languages');
                const data = await response.json();
                
                const fileEngine = document.getElementById('engine');
                const recordEngine = document.getElementById('record-engine');
                
                // 为文件上传标签页设置语言选项
                updateLanguageOptions(fileEngine.value, 'language', data);
                
                // 为录音标签页设置语言选项
                updateLanguageOptions(recordEngine.value, 'record-language', data);
                
                // 引擎切换时更新语言选项
                fileEngine.addEventListener('change', function() {
                    updateLanguageOptions(this.value, 'language', data);
                });
                
                recordEngine.addEventListener('change', function() {
                    updateLanguageOptions(this.value, 'record-language', data);
                });
                
            } catch (error) {
                console.error('加载语言列表失败:', error);
            }
        }
        
        // 更新语言选项
        function updateLanguageOptions(engine, selectId, languages) {
            const select = document.getElementById(selectId);
            select.innerHTML = '';
            
            if (languages[engine]) {
                languages[engine].forEach(lang => {
                    const option = document.createElement('option');
                    option.value = lang.code;
                    option.textContent = lang.name;
                    select.appendChild(option);
                });
            }
        }
        
        // 文件上传处理
        document.getElementById('file-input').addEventListener('change', handleFileSelect);
        
        // 拖放处理
        const dropArea = document.getElementById('drop-area');
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            dropArea.style.borderColor = '#667eea';
            dropArea.style.background = '#f8f9ff';
        }
        
        function unhighlight() {
            dropArea.style.borderColor = '#e0e0e0';
            dropArea.style.background = '';
        }
        
        dropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                handleFiles(files);
            }
        }
        
        function handleFileSelect(e) {
            const files = e.target.files;
            if (files.length > 0) {
                handleFiles(files);
            }
        }
        
        function handleFiles(files) {
            const file = files[0];
            const fileName = file.name;
            
            // 显示文件名
            dropArea.innerHTML = `
                <i class="fas fa-file-audio"></i>
                <p>已选择文件: ${fileName}</p>
                <p style="color: #666; font-size: 14px; margin-top: 10px;">
                    点击"开始识别"按钮进行识别
                </p>
            `;
            
            // 存储文件以便上传
            window.selectedFile = file;
        }
        
        // 上传按钮点击
        document.getElementById('upload-btn').addEventListener('click', async function() {
            if (!window.selectedFile) {
                alert('请先选择文件');
                return;
            }
            
            const formData = new FormData();
            formData.append('audio', window.selectedFile);
            formData.append('engine', document.getElementById('engine').value);
            formData.append('language', document.getElementById('language').value);
            
            await sendRequest(formData, 'file');
        });
        
        // 录音功能
        document.getElementById('record-btn').addEventListener('click', async function() {
            if (!isRecording) {
                startRecording();
            } else {
                stopRecording();
            }
        });
        
        // 开始录音
        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        sampleRate: 16000,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });
                
                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm'
                });
                
                audioChunks = [];
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener('stop', async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    
                    // 停止所有轨道
                    stream.getTracks().forEach(track => track.stop());
                    
                    // 准备发送
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.webm');
                    
                    const engine = document.getElementById('record-engine').value;
                    const language = document.getElementById('record-language').value;
                    
                    await sendRequest(formData, 'record', engine, language);
                });
                
                mediaRecorder.start();
                isRecording = true;
                
                // 更新UI
                document.getElementById('record-btn').classList.add('recording');
                document.getElementById('record-btn').innerHTML = '<i class="fas fa-stop"></i>';
                document.getElementById('status').textContent = '录音中...';
                
                // 启动计时器
                seconds = 0;
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000);
                
            } catch (error) {
                console.error('录音失败:', error);
                alert('无法访问麦克风，请检查权限设置');
            }
        }
        
        // 停止录音
        function stopRecording() {
            if (mediaRecorder && isRecording) {
                mediaRecorder.stop();
                isRecording = false;
                
                // 更新UI
                document.getElementById('record-btn').classList.remove('recording');
                document.getElementById('record-btn').innerHTML = '<i class="fas fa-microphone"></i>';
                document.getElementById('status').textContent = '录音完成，正在识别...';
                
                // 停止计时器
                clearInterval(timerInterval);
            }
        }
        
        // 更新计时器
        function updateTimer() {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            document.getElementById('timer').textContent = 
                `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }
        
        // 发送请求
        async function sendRequest(formData, type, engine = null, language = null) {
            // 显示加载中
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result-section').style.display = 'none';
            
            let url = '/api/recognize';
            let method = 'POST';
            
            if (type === 'record') {
                url = `/api/record?engine=${engine}&language=${language}`;
                method = 'POST';
                
                // 转换为ArrayBuffer发送
                const audioBlob = formData.get('audio');
                const arrayBuffer = await audioBlob.arrayBuffer();
                
                try {
                    const response = await fetch(url, {
                        method: method,
                        body: arrayBuffer,
                        headers: {
                            'Content-Type': 'audio/webm'
                        }
                    });
                    
                    handleResponse(await response.json());
                    
                } catch (error) {
                    handleError(error);
                }
                
            } else {
                // 文件上传
                try {
                    const response = await fetch(url, {
                        method: method,
                        body: formData
                    });
                    
                    handleResponse(await response.json());
                    
                } catch (error) {
                    handleError(error);
                }
            }
        }
        
        // 处理响应
        function handleResponse(data) {
            // 隐藏加载中
            document.getElementById('loading').style.display = 'none';
            
            if (data.success) {
                // 显示结果
                document.getElementById('result-text').textContent = data.text;
                document.getElementById('result-section').style.display = 'block';
                
                // 滚动到结果
                document.getElementById('result-section').scrollIntoView({ 
                    behavior: 'smooth' 
                });
            } else {
                alert(`识别失败: ${data.error}`);
            }
            
            // 重置状态
            if (activeTab === 'file-tab') {
                document.getElementById('drop-area').innerHTML = `
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>拖放文件到这里，或点击选择文件</p>
                    <p style="color: #666; font-size: 14px; margin-top: 10px;">
                        支持格式: WAV, MP3, M4A, OGG, FLAC
                    </p>
                    <input type="file" id="file-input" accept="audio/*">
                `;
                
                // 重新绑定事件
                document.getElementById('file-input').addEventListener('change', handleFileSelect);
                window.selectedFile = null;
            } else {
                document.getElementById('status').textContent = '准备录音';
                document.getElementById('timer').textContent = '00:00';
            }
        }
