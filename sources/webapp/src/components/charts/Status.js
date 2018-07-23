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
  props: ['graphs_data'],
  mounted () {
    this.renderChart({
      labels: this.graphs_data.date_time,
      datasets: [
        {
          label: 'CPU',
          fill: false,
          backgroundColor: chartColors.red,
          borderColor: chartColors.red,
          data: this.graphs_data.cpu_percent
        },
        {
          label: 'Memory',
          fill: false,
          backgroundColor: chartColors.blue,
          borderColor: chartColors.blue,
          data: this.graphs_data.vmem_percent
        },
        {
          label: 'Temperature',
          fill: false,
          backgroundColor: chartColors.yellow,
          borderColor: chartColors.yellow,
          data: this.graphs_data.cpu_temp
        }
      ]
    },
    {
      responsive: true,
      maintainAspectRatio: false
    })
  }
}
