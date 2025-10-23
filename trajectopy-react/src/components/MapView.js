import React from 'react';
import LeafletView from './LeafletView';
import CanvasPlotView from './CanvasPlotView';
import './MapView.css';

const MapView = ({ trajectories }) => {
    const [viewState, setViewState] = React.useState({ center: [0, 0], zoom: 12 });

    const visibleTrajectories = React.useMemo(() =>
        trajectories.filter(t => t.isVisible),
        [trajectories]
    );

    const hasLocalTrajectories = React.useMemo(() =>
        visibleTrajectories.some(t => t.epsg === 0),
        [visibleTrajectories]
    );

    const hasGeoTrajectories = React.useMemo(() =>
        visibleTrajectories.some(t => t.epsg === 4326 || t.epsg === '4326'),
        [visibleTrajectories]
    );

    const localTrajectories = React.useMemo(() =>
        hasLocalTrajectories ? visibleTrajectories.filter(t => t.epsg === 0) : [],
        [visibleTrajectories, hasLocalTrajectories]
    );

    const geoTrajectories = React.useMemo(() =>
        hasGeoTrajectories ? visibleTrajectories.filter(
            t => t.epsg === 4326 || t.epsg === '4326'
        ) : [],
        [visibleTrajectories, hasGeoTrajectories]
    );


    if (hasLocalTrajectories) {
        return <CanvasPlotView trajectories={localTrajectories} />;

    } else if (hasGeoTrajectories) {
        return <LeafletView
            trajectories={geoTrajectories}
            viewState={viewState}
            setViewState={setViewState}
        />;

    } else {
        return (
            <div className="map-empty-state">
                No plottable trajectories to display.
            </div>
        );
    }
};

export default MapView;