import React, { useRef, useEffect, useState, useCallback } from 'react';
import './CanvasPlotView.css';

function getInitialView(width, height, trajectories) {
    const PADDING = 40;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

    trajectories.forEach(traj => {
        if (traj.positions) {
            traj.positions.forEach(([x, y]) => {
                minX = Math.min(minX, x);
                maxX = Math.max(maxX, x);
                minY = Math.min(minY, y);
                maxY = Math.max(maxY, y);
            });
        }
    });

    if (!isFinite(minX)) { // No data
        return { scale: 1, worldX: 0, worldY: 0 };
    }

    const dataWidth = (maxX - minX) || 1;
    const dataHeight = (maxY - minY) || 1;

    const scaleX = (width - PADDING * 2) / dataWidth;
    const scaleY = (height - PADDING * 2) / dataHeight;
    const scale = Math.min(scaleX, scaleY);

    const worldX = minX + dataWidth / 2;
    const worldY = minY + dataHeight / 2;

    return { scale, worldX, worldY };
}

function worldToScreen(worldX, worldY, view, width, height) {
    const canvasX = (worldX - view.worldX) * view.scale + width / 2;
    const canvasY = -(worldY - view.worldY) * view.scale + height / 2;
    return [canvasX, canvasY];
}

function screenToWorld(canvasX, canvasY, view, width, height) {
    const worldX = (canvasX - width / 2) / view.scale + view.worldX;
    const worldY = -(canvasY - height / 2) / view.scale + view.worldY;
    return [worldX, worldY];
}


function drawGrid(ctx, view, width, height) {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;

    const gridSize = 20 * (1 / view.scale);

    const [worldLeft, worldTop] = screenToWorld(0, 0, view, width, height);
    const [worldRight, worldBottom] = screenToWorld(width, height, view, width, height);

    const startX = Math.floor(worldLeft / gridSize) * gridSize;
    for (let x = startX; x <= worldRight; x += gridSize) {
        const [canvasX,] = worldToScreen(x, 0, view, width, height);
        ctx.moveTo(canvasX, 0);
        ctx.lineTo(canvasX, height);
    }

    const startY = Math.floor(worldBottom / gridSize) * gridSize;
    for (let y = startY; y <= worldTop; y += gridSize) {
        const [, canvasY] = worldToScreen(0, y, view, width, height);
        ctx.moveTo(0, canvasY);
        ctx.lineTo(width, canvasY);
    }
    ctx.stroke();

    const [originX, originY] = worldToScreen(0, 0, view, width, height);
    ctx.beginPath();
    ctx.strokeStyle = '#aaa';
    ctx.lineWidth = 1;
    ctx.moveTo(originX, 0);
    ctx.lineTo(originX, height);
    ctx.moveTo(0, originY);
    ctx.lineTo(width, originY);
    ctx.stroke();
}

function drawTrajectories(ctx, view, width, height, trajectories) {
    trajectories.forEach((traj, index) => {
        if (!traj.positions || traj.positions.length < 2) return;

        ctx.beginPath();
        ctx.strokeStyle = traj.color;
        ctx.lineWidth = 2;

        const [startX, startY] = worldToScreen(traj.positions[0][0], traj.positions[0][1], view, width, height);
        ctx.moveTo(startX, startY);

        for (let i = 1; i < traj.positions.length; i++) {
            const [x, y] = worldToScreen(traj.positions[i][0], traj.positions[i][1], view, width, height);
            ctx.lineTo(x, y);
        }
        ctx.stroke();
    });
}

function drawScaleBar(ctx, view, height) {
    const targetScreenWidth = 100;
    const worldDistance = targetScreenWidth / view.scale;

    const powerOf10 = 10 ** Math.floor(Math.log10(worldDistance));
    const normalizedDistance = worldDistance / powerOf10;

    let niceWorldDistance;
    if (normalizedDistance < 1.5) niceWorldDistance = 1 * powerOf10;
    else if (normalizedDistance < 3) niceWorldDistance = 2 * powerOf10;
    else if (normalizedDistance < 7) niceWorldDistance = 5 * powerOf10;
    else niceWorldDistance = 10 * powerOf10;

    const scaleBarScreenWidth = niceWorldDistance * view.scale;

    const margin = 20;
    const x = margin;
    const y = height - margin;
    const label = `${niceWorldDistance} m`;

    ctx.beginPath();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;

    ctx.moveTo(x, y);
    ctx.lineTo(x + scaleBarScreenWidth, y);

    ctx.moveTo(x, y - 5);
    ctx.lineTo(x, y + 5);
    ctx.moveTo(x + scaleBarScreenWidth, y - 5);
    ctx.lineTo(x + scaleBarScreenWidth, y + 5);
    ctx.stroke();

    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    ctx.fillText(label, x + scaleBarScreenWidth / 2, y - 8);
}


const CanvasPlotView = ({ trajectories }) => {
    const canvasRef = useRef(null);
    const containerRef = useRef(null);

    const [view, setView] = useState({ scale: 1, worldX: 0, worldY: 0 });

    const initialViewRef = useRef(null);

    const [isPanning, setIsPanning] = useState(false);
    const [lastPanPos, setLastPanPos] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const container = containerRef.current;
        if (!container || trajectories.length === 0) return;

        const { width, height } = container.getBoundingClientRect();
        const initialView = getInitialView(width, height, trajectories);

        setView(initialView);
        initialViewRef.current = initialView;
    }, [trajectories]);


    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const { width, height } = canvas;

        drawGrid(ctx, view, width, height);
        drawTrajectories(ctx, view, width, height, trajectories);

        drawScaleBar(ctx, view, height);

    }, [view, trajectories]);


    useEffect(() => {
        const canvas = canvasRef.current;
        const container = containerRef.current;
        if (!canvas || !container) return;

        const resizeObserver = new ResizeObserver(entries => {
            const { width, height } = entries[0].contentRect;
            canvas.width = width;
            canvas.height = height;
            const initialView = getInitialView(width, height, trajectories);
            setView(initialView);
            initialViewRef.current = initialView;
        });

        resizeObserver.observe(container);
        return () => resizeObserver.disconnect();
    }, [trajectories]);



    const onMouseDown = useCallback((e) => {
        setIsPanning(true);
        setLastPanPos({ x: e.clientX, y: e.clientY });
    }, []);

    const onMouseUp = useCallback(() => {
        setIsPanning(false);
    }, []);

    const onMouseLeave = useCallback(() => {
        setIsPanning(false);
    }, []);

    const onMouseMove = useCallback((e) => {
        if (!isPanning) return;

        const deltaX = e.clientX - lastPanPos.x;
        const deltaY = e.clientY - lastPanPos.y;

        setView(prev => ({
            ...prev,
            worldX: prev.worldX - (deltaX / prev.scale),
            worldY: prev.worldY + (deltaY / prev.scale),
        }));
        setLastPanPos({ x: e.clientX, y: e.clientY });
    }, [isPanning, lastPanPos]);

    const onWheel = useCallback((e) => {
        e.preventDefault();
        const canvas = canvasRef.current;
        if (!canvas) return;

        const rect = canvas.getBoundingClientRect();
        const canvasX = e.clientX - rect.left;
        const canvasY = e.clientY - rect.top;

        const [worldX_before, worldY_before] = screenToWorld(
            canvasX, canvasY, view, canvas.width, canvas.height
        );

        const zoomFactor = 1.1;
        const newScale = e.deltaY < 0 ? view.scale * zoomFactor : view.scale / zoomFactor;

        const newWorldCenterX = worldX_before - (canvasX - canvas.width / 2) / newScale;
        const newWorldCenterY = worldY_before + (canvasY - canvas.height / 2) / newScale;

        setView({
            scale: newScale,
            worldX: newWorldCenterX,
            worldY: newWorldCenterY
        });
    }, [view]);

    const onResetView = () => {
        if (initialViewRef.current) {
            setView(initialViewRef.current);
        }
    };

    return (
        <div ref={containerRef} className="canvas-plot-container">
            <button className="canvas-reset-button" onClick={onResetView}>
                Reset View
            </button>
            <canvas
                ref={canvasRef}
                onMouseDown={onMouseDown}
                onMouseUp={onMouseUp}
                onMouseLeave={onMouseLeave}
                onMouseMove={onMouseMove}
                onWheel={onWheel}
            />
        </div>
    );
};

export default CanvasPlotView;