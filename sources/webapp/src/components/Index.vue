<template>
  <div class="index">
    <h1>{{ msg }}</h1>
    <!-- Container -->
    <b-container class="bv-example-row">
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h4>Resources</h4>
            </b-col>
            <b-col sm="4">
                <div v-if="loading" class="loading">
                  <img src="/static/images/spinner.gif" width="32" height="32"/>
                </div>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Hostname</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.hostname }}</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Platform</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.platform }}</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Uptime</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ parseInt(data.uptime/60/60/24) }} days</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Temperature</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.cpu_temp }}&deg; C</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>CPU</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.cpu_percent.toFixed(2) || '0' }}%</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Memory</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.mem_percent.toFixed(2) || '0' }}%</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>SWAP</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.swap_usage['percent'].toFixed(2) || '0' }}%</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Network</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">Tx {{ data.network_io['bytes_sent'] }}</p>
                <p v-if="data">Rx {{ data.network_io['bytes_recv'] }}</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Disks</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.disks_usage }}</p>
                <p v-if="data">{{ data.disks_io }}</p>
            </b-col>
        </b-row>
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h6>Processes</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.processes }}</p>
            </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  props: ['data'],
  name: 'Info',
  data () {
    return {
      msg: 'Resources'
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
