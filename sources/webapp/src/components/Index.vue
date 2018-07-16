<template>
  <div class="index">
    <!-- Container -->
    <b-container class="bv-example-row">
        <div v-if="loading" class="loading">
            <h1>Loading...</h1>
            <img src="/static/images/spinner.gif" width="32" height="32"/>
        </div>
        <div v-else>
            <h1>{{ msg }}</h1>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Hostname</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.hostname }}</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Platform</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.platform }}</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Uptime</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ parseInt(data.uptime/60/60/24) }} days</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Temperature</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.cpu_temp }}&deg; C</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>CPU</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.cpu_percent.toFixed(2) || '0' }}%</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Memory</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.mem_percent.toFixed(2) || '0' }}%</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>SWAP</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.swap_usage['percent'].toFixed(2) || '0' }}%</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Network</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">Tx {{ data.network_io['bytes_sent'] }}</p>
                    <p v-if="data">Rx {{ data.network_io['bytes_recv'] }}</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Disks</h3>
                </b-col>
                <b-col sm="8">
                    <div v-if="data">
                        <b-btn v-b-toggle.disksUsageText class="m-1">View Usage</b-btn>
                        <b-btn v-b-toggle.disksIOText class="m-1">View IO</b-btn>
                        <b-collapse id="disksUsageText">
                          <b-card>
                              <ul>
                                <li v-for="disk in data.disks_usage" v-bind:key="disk"><strong>{{ disk['mountpoint'] }}</strong>: {{ disk['percent'] }} %</li>
                              </ul>
                          </b-card>
                        </b-collapse>
                        <b-collapse id="disksIOText">
                          <b-card>
                              <ul>
                                <li v-for="disk in data.disks_io" v-bind:key="disk"><strong>{{ disk['device'] }}</strong>: {{ disk['read_bytes'] }} / {{ disk['write_bytes'] }}</li>
                              </ul>
                          </b-card>
                        </b-collapse>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Processes</h3>
                </b-col>
                <b-col sm="8">
                    <div v-if="data">
                        <b-btn v-b-toggle.processesText class="m-1">View All</b-btn>
                        <b-collapse id="processesText">
                          <b-card>
                              <ul>
                                <li v-for="proc in data.processes" v-bind:key="proc" v-if="proc['cpu_percent'] > 0">
                                    <strong>{{ proc['name'] }} ({{ proc['pid'] }})</strong>: {{ proc['cpu_percent'] }}
                                </li>
                              </ul>
                          </b-card>
                        </b-collapse>
                    </div>
                </b-col>
            </b-row>
        </div>
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
