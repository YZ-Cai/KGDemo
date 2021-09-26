<template>
  <v-row>
    <v-col cols="4">
      <div class="pa-4" style="background-color:#fafafa; height:800px">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">邻居查找</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-container>
                <v-text-field label="请输入节点名称" v-model="getNeighborsInput"></v-text-field>
                <v-btn outlined @click="getNeighbors">查找</v-btn>
                <v-btn outlined @click="getFullGraph" class="ml-4">显示全图</v-btn>
              </v-container>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">从文本导入关系（关系抽取）</v-expansion-panel-header>
            <v-expansion-panel-content>
              to do.
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">按格式导入关系（直接导入）</v-expansion-panel-header>
            <v-expansion-panel-content>
              to do.
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">语义检索</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-container>
                <v-text-field label="请输入关键词"></v-text-field>
                <v-btn outlined>搜索</v-btn>
              </v-container>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">关键节点查询</v-expansion-panel-header>
            <v-expansion-panel-content>
              to do.
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">关键路径查询</v-expansion-panel-header>
            <v-expansion-panel-content>
              to do.
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header class="text-subtitle-1">链接预测</v-expansion-panel-header>
            <v-expansion-panel-content>
              to do.
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </v-col>
    <v-col cols="8">
      <div id="graph" :style="{width: '1000px', height: '800px'}"/>
    </v-col>
  </v-row>
</template>

<script>
  import * as echarts from 'echarts';
  import axios from 'axios';
  export default {
    data() {
      return {
        nodes: [],
        edges: [],
        showLoading: true,
        getNeighborsInput: '',
      }
    },

    methods: {

      // 从 Python 后端获取全图数据
      getFullGraph() {
        // 发送Post请求获取数据
        let that = this;
        axios.post('/api/getFullGraph').then(function (response) {
          // 写入图数据
          var graph = response.data.graph;
          var inputNodes = graph.nodes;
          var inputEdges =  graph.edges;
          that.nodes = [];
          that.edges = [];
          for (let i in inputNodes) 
            that.nodes.push({name: inputNodes[i]});
          for (let i in inputEdges)
            that.edges.push({source: inputEdges[i][0], target: inputEdges[i][2], label: {show: true, formatter: inputEdges[i][1]}});
          // 绘图
          that.drawGraph();  
        }).catch(function (error) {
          console.log(error);
        });      
      },

      // 从 Python 后端查询某个点的所有邻居
      getNeighbors() {
        if (this.getNeighborsInput!='') {
          // 发送Post请求获取数据
          let that = this;
          axios.post('/api/getNeighbors', {
            nodename: this.getNeighborsInput
          }).then(function (response) {
            // 写入图数据
            var graph = response.data.graph;
            var inputNodes = graph.nodes;
            var inputEdges =  graph.edges;
            that.nodes = [];
            that.edges = [];
            for (let i in inputNodes) 
              that.nodes.push({name: inputNodes[i]});
            for (let i in inputEdges)
              that.edges.push({source: inputEdges[i][0], target: inputEdges[i][2], label: {show: true, formatter: inputEdges[i][1]}});
            // 绘图
            that.drawGraph();  
          }).catch(function (error) {
            console.log(error);
          }); 
        } else 
          alert("输入框不能为空！");
      },
      
      // 绘图
      drawGraph() {
        var chartDom = document.getElementById('graph');
        var myChart = echarts.init(chartDom);
        var option;
        option = {
          tooltip: {},
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          series: [{
            type: 'graph',
            layout: 'circular',
            symbolSize: 100,
            roam: true,
            label: {
              show: true,
              width: 100,
              overflow: "break"
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 16],
            edgeLabel: {
              fontSize: 12,
              width: 150,
              overflow: "break"
            },
            data: this.nodes,
            links: this.edges,
            lineStyle: {
              opacity: 0.9,
              width: 2,
            }
          }]
        };
        myChart.setOption(option);
      }
    },
    
    // 页面加载时的操作
    mounted(){
      this.getFullGraph();
    },

    // 页面变量深度监听，可监听到对象、数组的变化
    watch:{
      showLoading:{
        handler(val){
          this.showLoading = val;
        },
        deep:true     // 深度监听
      },
      getNeighborsInput:{
        handler(val){
          this.getNeighborsInput = val;
        },
        deep:true     // 深度监听
      },
      nodes:{
        handler(val){
          this.nodes = val;
        },
        deep:true     // 深度监听
      },
      edges:{
        handler(val){
          this.edges = val;
        },
        deep:true     // 深度监听
      },
    }
  }
</script>
