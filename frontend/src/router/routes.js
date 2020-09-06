
const routes = [
  {
    path: '/',
    component: () => import('layouts/main.vue'),
    children: [
      { path: '', component: () => import('pages/information.vue') },
      { path: 'pollen', component: () => import('pages/pollen.vue') },
      { path: 'spores', component: () => import('pages/spores.vue') },
      { path: 'information', component: () => import('pages/information.vue') }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
