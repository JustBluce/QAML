<template>
  <div class="app-container">
    <div class="filter-container">
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox label="ID">
          ID
        </el-checkbox>
        <el-checkbox label="name">
          name
        </el-checkbox>
        <el-checkbox label="idcard">
          idcard
        </el-checkbox>
        <el-checkbox label="age">
          age
        </el-checkbox>
        <el-checkbox label="sex">
          sex
        </el-checkbox>
      </el-checkbox-group>
    </div>

    <el-table :data="tableData" border fit highlight-current-row style="width: 100%">
<!--      <el-table-column prop="WeChatId" label="WeChatId" width="180" />-->
      <el-table-column v-for="ID in formThead" :key="ID" :label="ID">
        <template slot-scope="scope">
          {{ scope.row[ID] }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  const defaultFormThead = ['ID', 'name']

  export default {
    data() {
      return {
        tableData: [],
        key: 1, // table key
        formTheadOptions: ['ID', 'name', 'idcard', 'age', 'sex'],
        checkboxVal: defaultFormThead, // checkboxVal
        formThead: defaultFormThead // 默认表头 Default header
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData: function() {
        this.axios({
          method: 'GET',
          url: 'http://127.0.0.1:5000/user'
        }).then(response => {
          this.tableData = response.data
          console.log(response)
        });
      }
    },
    watch: {
      checkboxVal(valArr) {
        this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
        this.key = this.key + 1// 为了保证table 每次都会重渲 In order to ensure the table will be re-rendered each time
      }
    }
  }
</script>

