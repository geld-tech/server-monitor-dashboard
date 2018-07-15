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
                <h6>Temperature</h6>
            </b-col>
            <b-col sm="4">
                <p v-if="data">{{ data.cpu_temp }}&deg; C</p>
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
