import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import EventsView from "../views/EventsView.vue";
import RankingView from "../views/RankingView.vue";
import StatusView from "../views/StatusView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/events", name: "events", component: EventsView },
  {
    path: "/events/:id",
    name: "event-detail",
    component: () => import("../views/EventDetailView.vue"),
    children: [
      {
        path: "players",
        name: "event-players",
        component: () => import("../views/PlayersView.vue"),
      },
      {
        path: "matches",
        name: "event-matches",
        component: () => import("../views/MatchesView.vue"),
      },
      {
        path: "history",
        name: "event-history",
        component: () => import("../views/MatchHistoryView.vue"),
      },
    ],
  },
  // Rotas de jogadores e jogos agora são acessadas via detalhes do evento
  { path: "/ranking", name: "ranking", component: RankingView },
  { path: "/status", name: "status", component: StatusView },
  {
    path: "/dev-blog",
    name: "dev-blog",
    component: () => import("../views/DevBlogView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
