<template>
  <div class="app-container">
    <div class="filter-container">
      <el-checkbox-group v-model="formThead">
        <el-checkbox label="id">
          id
        </el-checkbox>
        <el-checkbox label="PE">
          PE
        </el-checkbox>
        <el-checkbox label="Project">
          Project
        </el-checkbox>
        <el-checkbox label="R_1_Program_Element">
          R_1_Program_Element
        </el-checkbox>
        <el-checkbox label="Y_buget">
          Y_buget
        </el-checkbox>
        <el-checkbox label="_1_Y_buget">
          _1_Y_buget
        </el-checkbox>
        <el-checkbox label="_2_Y_buget">
          _2_Y_buget
        </el-checkbox>
        <el-checkbox label="service">
          service
        </el-checkbox>
        <el-checkbox label="title">
          title
        </el-checkbox>
        <el-checkbox label="year">
          year
        </el-checkbox>
      </el-checkbox-group>
    </div>

    <el-table :data="tableData" border fit highlight-current-row style="width: 100%">
      <el-table-column prop="id" label="id" width="180" />
      <el-table-column v-for="id in formThead" :key="id" :label="id">
        <template slot-scope="scope">
          {{ scope.row[id] }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
const defaultFormThead = ['id', 'PE', 'Project']

export default {
  data() {
    return {
      tableData: [],
      key: 1, // table key
      formTheadOptions: ['id', 'PE', 'Project', 'R_1_Program_Element', 'Y_buget', '_1_Y_buget', '_2_Y_buget', 'service', 'title', 'year'],
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
        url: 'http://127.0.0.1:5000/dataresearch'
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
  },
}
</script>
