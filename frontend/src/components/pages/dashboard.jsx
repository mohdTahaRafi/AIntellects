import React from 'react';
import { Card, CardContent } from '@mui/material';
import PieCard from './PieCard';
import BarGraph from './BarGraph';

const commonData = [
    { id: 0, value: 45, label: 'Category 1' },
    { id: 1, value: 25, label: 'Category 2' },
    { id: 2, value: 15, label: 'Category 3' },
    { id: 3, value: 15, label: 'Category 4' }
];

const barData = [
    { id: 0, label: 'Lane 1', value: 45 },
    { id: 1, label: 'Lane 2', value: 25 },
    { id: 2, label: 'Lane 3', value: 15 },
    { id: 3, label: 'Lane 4', value: 15 }
];

const colors = ['#7F2F1B', '#095832', '#584709', '#170503'];

const Dashboard = () => {
    return (
        <div>
            <h2>Dashboard</h2>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
                <Card sx={{ 
                    backgroundColor: '#2f3030',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', 
                    width: 450,
                    margin: 2
                }}>
                    <CardContent>
                        <video 
                            width="100%" 
                            height="300"
                            controls
                        >
                            <source src="https://youtu.be/dmlUpuUony4?si=oNr6vP6F9S2OQg0W" type="video/mp4"/>
                            Your browser does not support the video tag.
                        </video>
                    </CardContent>
                </Card>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
                <Card sx={{ 
                    backgroundColor: '#2f3030',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                    width: 450,
                    margin: 2,
                }}>
                    <CardContent>
                        <BarGraph data={barData} colors={colors} />
                    </CardContent>
                </Card>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-around' }}>
                <PieCard title="LANE-1" data={commonData} colors={colors} />
                <PieCard title="LANE-2" data={commonData} colors={colors} />
                <PieCard title="LANE-3" data={commonData} colors={colors} />
                <PieCard title="LANE-4" data={commonData} colors={colors} />
            </div>
        </div>
    );
};

export default Dashboard;