import Vue from 'vue'
import Router from 'vue-router'

import ProjectsTweets from '@/components/ProjectsTweets'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ProjectsTweets',
      component: ProjectsTweets
    },
    {
      path: '/404',
      name: '404',
      component: NotFound
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})
