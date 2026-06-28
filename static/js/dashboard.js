// Resume Upload Trend Chart
const uploadTrendChart = document.getElementById("uploadTrendChart");

if (uploadTrendChart) {
    new Chart(uploadTrendChart, {
        type: "line",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            datasets: [{
                label: "Resumes Uploaded",
                data: [0, 0, 0, 0, 0, 0, 0],
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}

// Candidate Status Chart
const candidateStatusChart = document.getElementById("candidateStatusChart");

if (candidateStatusChart) {
    new Chart(candidateStatusChart, {
        type: "doughnut",
        data: {
            labels: ["Pending", "Shortlisted", "Rejected"],
            datasets: [{
                data: [0, 0, 0]
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Match Score Distribution Chart
const scoreDistributionChart = document.getElementById("scoreDistributionChart");

if (scoreDistributionChart) {
    new Chart(scoreDistributionChart, {
        type: "bar",
        data: {
            labels: ["0-20", "21-40", "41-60", "61-80", "81-100"],
            datasets: [{
                label: "Candidates",
                data: [0, 0, 0, 0, 0]
            }]
        },
        options: {
            responsive: true
        }
    });
}