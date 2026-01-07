// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set today's date as default
    document.getElementById('date').valueAsDate = new Date();
    
    // Load initial data
    loadBalance();
    loadTransactions();
    loadCharts();
    
    // Add event listeners
    document.getElementById('transaction-form').addEventListener('submit', handleAddTransaction);
    document.getElementById('category-filter').addEventListener('input', filterTransactions);
    document.getElementById('type-filter').addEventListener('change', filterTransactions);
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Load and display balance
async function loadBalance() {
    try {
        const response = await fetch('/api/get-balance');
        const data = await response.json();
        
        document.getElementById('total-balance').textContent = formatCurrency(data.balance);
        document.getElementById('total-income').textContent = formatCurrency(data.income);
        document.getElementById('total-expense').textContent = formatCurrency(data.expense);
    } catch (error) {
        console.error('Error loading balance:', error);
    }
}

// Add transaction
async function handleAddTransaction(e) {
    e.preventDefault();
    
    const formData = {
        type: document.getElementById('type').value,
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value,
        date: document.getElementById('date').value,
        notes: document.getElementById('notes').value
    };
    
    // Validate form
    if (!formData.type || !formData.amount || !formData.category || !formData.date) {
        alert('Please fill in all required fields');
        return;
    }
    
    if (formData.amount <= 0) {
        alert('Amount must be greater than 0');
        return;
    }
    
    try {
        const response = await fetch('/api/add-transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            // Reset form
            document.getElementById('transaction-form').reset();
            document.getElementById('date').valueAsDate = new Date();
            
            // Reload data
            loadBalance();
            loadTransactions();
            loadCharts();
            
            alert('Transaction added successfully!');
        } else {
            alert('Error adding transaction: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error adding transaction:', error);
        alert('Error adding transaction');
    }
}

// Load and display transactions
let allTransactions = [];

async function loadTransactions() {
    try {
        const response = await fetch('/api/get-transactions');
        allTransactions = await response.json();
        displayTransactions(allTransactions);
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

// Display transactions in table
function displayTransactions(transactions) {
    const tbody = document.getElementById('transactions-body');
    
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999;">No transactions yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = transactions.map(trans => {
        const dateObj = new Date(trans.date + 'T00:00:00');
        const formattedDate = dateObj.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        const typeClass = trans.type === 'income' ? 'income' : 'expense';
        const amountSymbol = trans.type === 'income' ? '+' : '-';
        
        return `
            <tr>
                <td>${formattedDate}</td>
                <td><span class="${typeClass}">${trans.type.toUpperCase()}</span></td>
                <td>${trans.category}</td>
                <td class="${typeClass}">${amountSymbol}${formatCurrency(trans.amount)}</td>
                <td>${trans.notes || '-'}</td>
                <td>
                    <button class="btn btn-delete" onclick="deleteTransaction(${trans.id})">Delete</button>
                </td>
            </tr>
        `;
    }).join('');
}

// Filter transactions
function filterTransactions() {
    const categoryFilter = document.getElementById('category-filter').value.toLowerCase();
    const typeFilter = document.getElementById('type-filter').value;
    
    const filtered = allTransactions.filter(trans => {
        const matchesCategory = trans.category.toLowerCase().includes(categoryFilter);
        const matchesType = typeFilter === '' || trans.type === typeFilter;
        return matchesCategory && matchesType;
    });
    
    displayTransactions(filtered);
}

// Delete transaction
async function deleteTransaction(id) {
    if (!confirm('Are you sure you want to delete this transaction?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/delete-transaction/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadBalance();
            loadTransactions();
            loadCharts();
            alert('Transaction deleted successfully!');
        } else {
            alert('Error deleting transaction');
        }
    } catch (error) {
        console.error('Error deleting transaction:', error);
        alert('Error deleting transaction');
    }
}

// Charts variables
let expenseChart = null;
let balanceChart = null;

// Load and display charts
async function loadCharts() {
    try {
        const response = await fetch('/api/get-chart-data');
        const data = await response.json();
        
        // Display expense chart
        displayExpenseChart(data.expenses_by_category);
        
        // Display balance chart
        displayBalanceChart(data.balance_over_time);
    } catch (error) {
        console.error('Error loading chart data:', error);
    }
}

// Display expense pie chart
function displayExpenseChart(expenses) {
    const ctx = document.getElementById('expense-chart').getContext('2d');
    
    // Destroy previous chart if exists
    if (expenseChart) {
        expenseChart.destroy();
    }
    
    if (expenses.length === 0) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.fillText('No expense data', 10, 20);
        return;
    }
    
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
    ];
    
    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: expenses.map(e => e.category),
            datasets: [{
                data: expenses.map(e => e.amount),
                backgroundColor: colors.slice(0, expenses.length),
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Display balance line chart
function displayBalanceChart(balanceData) {
    const ctx = document.getElementById('balance-chart').getContext('2d');
    
    // Destroy previous chart if exists
    if (balanceChart) {
        balanceChart.destroy();
    }
    
    if (balanceData.length === 0) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.fillText('No balance data', 10, 20);
        return;
    }
    
    balanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: balanceData.map(b => {
                const dateObj = new Date(b.date + 'T00:00:00');
                return dateObj.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                });
            }),
            datasets: [{
                label: 'Balance',
                data: balanceData.map(b => b.balance),
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#4CAF50',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

// Auto-refresh data every 30 seconds
setInterval(function() {
    loadBalance();
    loadTransactions();
    loadCharts();
}, 30000);
