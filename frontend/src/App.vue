<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      flat
    > 
      <v-icon class="mx-2">mdi-graph-outline</v-icon>
      <div class="d-flex align-center">
        知识图谱管理与查询系统
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="http://www.baidu.com"
        target="_blank"
        text
      >
        <v-icon>mdi-information-outline</v-icon>
        <span class="mr-2">帮助文档</span>  
      </v-btn>
    </v-app-bar>

    <v-main>
      <Main/>
    </v-main>
  </v-app>
</template>

<script>
import Main from './components/Main';

export default {
  name: 'App',

  components: {
    Main,
  },

  data: () => ({
    //
  }),
};
</script>
