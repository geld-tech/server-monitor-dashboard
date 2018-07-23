import {Line} from 'vue-chartjs'

var chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(231,233,237)'
}

export default {
  extends: Line,
  mounted () {
    this.renderChart({
      labels: ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
      datasets: [
        {
          label: 'CPU',
          fill: true,
          backgroundColor: chartColors.red,
          borderColor: chartColors.red,
          data: [40, 39, 10, 40, 39, 80, 40]
        },
        {
          label: 'Memory',
          fill: true,
          backgroundColor: chartColors.blue,
          borderColor: chartColors.blue,
          data: [60, 55, 32, 10, 2, 12, 53]
        }
      ]
    },
    {
      responsive: true,
      maintainAspectRatio: false
    })
  }
}
