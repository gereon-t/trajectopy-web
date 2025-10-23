import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';


const FitMapToBounds = ({ trajectories }) => {
    const map = useMap();

    useEffect(() => {
        const allPoints = trajectories.reduce((points, traj) => {
            if (traj.positions && traj.positions.length > 0) {
                return points.concat(traj.positions);
            }
            return points;
        }, []);

        if (allPoints.length > 0) {
            map.flyToBounds(allPoints, {
                padding: [50, 50],
                maxZoom: 20,
            });
        }

    }, [trajectories, map]);

    return null;
};


const MapStateSaver = ({ setViewState }) => {
    const map = useMap();

    useEffect(() => {
        const onMoveEnd = () => {
            const center = map.getCenter();
            const zoom = map.getZoom();
            setViewState({ center: [center.lat, center.lng], zoom: zoom });
        };

        map.on('moveend', onMoveEnd);

        return () => {
            map.off('moveend', onMoveEnd);
        };
    }, [map, setViewState]);

    return null;
};


const LeafletView = ({ trajectories, viewState, setViewState }) => {
    return (
        <MapContainer
            center={viewState.center}
            zoom={viewState.zoom}
            style={{ height: '100%', width: '100%' }}
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            <FitMapToBounds trajectories={trajectories} />
            <MapStateSaver setViewState={setViewState} />

            {trajectories.map((traj) => {
                if (traj.positions && traj.positions.length > 0) {
                    return (
                        <Polyline
                            key={traj.id}
                            positions={traj.positions}
                            color={traj.color}
                        />
                    );
                }
                return null;
            })}
        </MapContainer>
    );
};

export default LeafletView;