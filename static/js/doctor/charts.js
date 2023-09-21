
const ctx1 = document.getElementById('barChart1').getContext('2d');
const ctx2 = document.getElementById('circularBarChart').getContext('2d');

const data1 = {
    labels: ['Label 1', 'Label 2', 'Label 3', 'Label 4'],
    datasets: [{
        label: 'glucose control',
        data: [10, 20, 15, 25],
        backgroundColor: 'rgba(0, 123, 255, 0.6)',
        borderColor: 'rgba(0, 123, 255, 0.6)',
        borderWidth: 1
    }]
};



const data2 = {
    labels: ['Label 1', 'Label 2', 'Label 3', 'Label 4'],
    datasets: [{
        label: 'compliance',
        data: [10, 20, 15, 25],
        backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ],
        borderWidth: 0
    }]
};

const config1 = {
    type: 'bar',
    data: data1,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
};

const config2 = {
    type: 'doughnut',
    data: data2,
    options: {
        cutout: '70%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'bottom'
            }
        }
    }
};


const chart1 = new Chart(ctx1, config1);
const chart2 = new Chart(ctx2, config2);