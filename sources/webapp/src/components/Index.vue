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
                    <h3>CPU</h3>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.cpu_percent" v-bind:label="data.cpu_percent.toFixed(1)+'%' || '0'" height="20px"></b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Memory</h3>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.mem_percent" v-bind:label="data.mem_percent.toFixed(1)+'%' || '0'" height="20px"></b-progress-bar>
                    </b-progress>
                    <b-progress show-progress v-if="data && data.swap_usage['percent'] > 1" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="warning" v-bind:value="data.swap_usage['percent']"
                            v-bind:label="data.swap_usage['percent'].toFixed(1)+'%' || '0'" height="20px">
                        </b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Temperature</h3>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.cpu_temp" v-bind:label="data.cpu_temp+'&deg; C'" height="20px"></b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h3>Network</h3>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">Tx {{ data.network_io['bytes_sent'] }} / Rx {{ data.network_io['bytes_recv'] }}</p>
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
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="8">
                    <div v-if="data">
                        <b-collapse id="disksUsageText">
                          <b-card>
                              <ul>
                                <li v-for="disk in data.disks_usage" v-bind:key="disk"><strong>{{ disk['mountpoint'] }}</strong>: {{ disk['percent'] }} %</li>
                              </ul>
                          </b-card>
                        </b-collapse>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="8">
                    <div v-if="data">
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
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <div v-if="data">
                    <b-collapse id="processesText">
                      <b-card>
                          <b-table striped hover id="processesTable"
                            v-bind:items="data.processes"
                            v-bind:fields="[{key:'pid',sortable:true}, {key:'name',sortable:true}, {key:'cpu_percent',sortable:true,sortDirection:'desc'}]"
                            v-bind:per-page="12">
                        </b-table>
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
#processesTable{
  font-size: 10x;
}
</style>
