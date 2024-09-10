const url = 'http://127.0.0.1:8000/worship/document/0818.pdf';
const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';

let pdfDoc = null;

pdfjsLib.getDocument(url).promise.then(pdf => {
    pdfDoc = pdf;
    renderPage(1);
    renderPage(2);
});

function renderPage(pageNum) {
    pdfDoc.getPage(pageNum).then(page => {
        const container = document.getElementById(`pdf-page-${pageNum}`);
        
        // 기본 스케일 설정 (컨테이너 크기에 비례하여 고해상도로 설정)
        const scale = container.clientWidth / page.getViewport({ scale: 1 }).width;
        const highQualityScale = scale * 2; // 고해상도 스케일 (2배)
        const viewport = page.getViewport({ scale: highQualityScale });

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        container.appendChild(canvas);

        const renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        page.render(renderContext);

        // CSS로 컨테이너 크기에 맞추어 축소 표시
        canvas.style.width = `${container.clientWidth}px`;
        canvas.style.height = `${(canvas.height / canvas.width) * container.clientWidth}px`;

        // Handle resizing
        window.addEventListener('resize', () => resizeCanvas(container, canvas, page));
    });
}

function resizeCanvas(container, canvas, page) {
    const scale = container.clientWidth / page.getViewport({ scale: 1 }).width;
    const highQualityScale = scale * 2; // 고해상도 스케일 (2배)
    const viewport = page.getViewport({ scale: highQualityScale });

    // 리사이즈 시 기존 컨텍스트 초기화
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

    // 캔버스 크기 조정
    canvas.width = viewport.width;
    canvas.height = viewport.height;

    canvas.style.width = `${container.clientWidth}px`;
    canvas.style.height = `${(canvas.height / canvas.width) * container.clientWidth}px`;

    const renderContext = {
        canvasContext: context,
        viewport: viewport
    };

    // 리사이즈 후 페이지 재렌더링
    page.render(renderContext).promise.then(() => {
        // 뒤집힘 방지: 변환 초기화
        context.setTransform(1, 0, 0, 1, 0, 0);
    });
}

function renderPage(pageNum) {
    pdfDoc.getPage(pageNum).then(page => {
        const container = document.getElementById(`pdf-page-${pageNum}`);
        
        const scale = container.clientWidth / page.getViewport({ scale: 1 }).width;
        const highQualityScale = scale * 2; // 고해상도 스케일 (2배)
        const viewport = page.getViewport({ scale: highQualityScale });

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        container.appendChild(canvas);

        const renderContext = {
            canvasContext: context,
            viewport: viewport
        };

        // 페이지가 로드될 때 애니메이션 클래스 추가
        canvas.classList.add('pdf-page');
        
        page.render(renderContext).promise.then(() => {
            // 애니메이션이 끝나면 클래스 제거 (선택사항)
            setTimeout(() => {
                canvas.classList.remove('pdf-page');
            }, 600); // 애니메이션 시간과 일치
        });

        // CSS로 컨테이너 크기에 맞추어 축소 표시
        canvas.style.width = `${container.clientWidth}px`;
        canvas.style.height = `${(canvas.height / canvas.width) * container.clientWidth}px`;

        // Handle resizing
        window.addEventListener('resize', () => resizeCanvas(container, canvas, page));
    });
}

