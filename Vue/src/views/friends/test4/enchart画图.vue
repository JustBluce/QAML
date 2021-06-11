<template>
  <div>
<!--    <p>{{data_detail}}</p>-->
    <div class="app-container">
      <div class="filter-container">

        <el-select
          v-model="listQuery.Organization"
          placeholder="Organization"
          clearable
          style="width: 135px"
          class="filter-item"
        >
          <el-option
            v-for="item in OrganizationOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>

        <el-button
          v-waves
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="fetchData"
        >
          Search
        </el-button>



      </div>

    </div>
    <!--    enchart图在这个位置-->
    <div id="main" style="width: 1200px;height: 700px;">
    </div>

  </div>

</template>

<script>
import echarts from 'echarts'
import {fetchList} from "@/api/article";
export default {
  name: '',
  data() {

    return {
      list: '',
      charts: '',
      data_detail: [{"value": 145212772.0, "name": "2021"}, {"value": 123422736.0, "name": "2020"}],
      // data_detail:[{"value": 145212772.0, "name": "2021"}, {"value": 123422736.0, "name": "2020"}, {"value": 154283583.0, "name": "2019"}, {"value": 135282402.0, "name": "2018"}, {"value": 132650561.0, "name": "2017"}, {"value": 133031536.0, "name": "2016"}, {"value": 110862180.0, "name": "2015"}, {"value": 116979203.0, "name": "2014"}, {"value": 124151247.0, "name": "2013"}],
      data_pro: ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013"],

      listQuery: {
        From: undefined,
        Year: undefined,
        Organization:  "ARMY",
      },
      FromOptions: ["c1", "m1","o1","p1","p1r","r1","rf1"],
      YearOptions: ["2021", "2020","2019","2018","2017","2016","2015","2014","2013"],
      OrganizationOptions: ['ARMY', 'NAVY', 'AF', 'DEFW', 'DHA', 'DISA', 'DLA', 'DODEA', 'DTRA', 'MDA', 'NGA', 'NSA', 'SOCOM', 'TJS', 'DIA', 'WHS', 'TMA', 'DFAS', 'DAU', 'CMP', 'DCAA', 'DCMA', 'DCSA', 'DHRA', 'DLSA', 'DMACT', 'DPAA', 'DSCA', 'DTIC', 'DTSA', 'OEA', 'OSD', 'SDA', 'IG', 'CAAF', 'DEPS', 'DEPSDDR', 'DSS', 'NDU', 'DPMO', 'DHP', 'DEFR', 'BTA', 'CBDP', 'DARPA', 'OTE', 'TRANSCOM', 'DECA'],

    }
  },
  methods: {
    drawLine(id) {
      let data_a = JSON.parse(JSON.stringify(this.data_detail));
      let org=this.listQuery.Organization


      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text: org+'组织的年预算',
          subtext: '2013~2021一共9年数据',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.data_pro
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: true,
            label: {
              show: true,
            },

            data: data_a

          }
        ]
      })
    }
    ,
    fetchData: function () {
      let search_what=this.listQuery.Organization
      let formData = new FormData();
      formData.append("From", this.listQuery.From);
      formData.append("Year", this.listQuery.Year);
      formData.append("Organization", this.listQuery.Organization);
      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/echarts",
        data:formData,
      }).then((response) => {
        this.data_detail = response.data;
        console.log(response);
      });
    },

  },
  // 调用
  mounted() {
    this.$nextTick(function () {
      this.drawLine('main')
    })
  },

  created() {
    this.fetchData();
  },

  watch: {
    data_detail ()
  {
    this.$nextTick(function () {
      this.drawLine('main')
    })
  },

}



}

</script>
<!--<style scoped>-->
<!--* {-->
<!--  margin: 0;-->
<!--  padding: 0;-->
<!--  list-style: none;-->
<!--}-->
<!--</style>-->
