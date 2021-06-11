<template>
  <div class="app-container">
    <div class="filter-container">


      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox label="ID">
          ID
        </el-checkbox>
        <el-checkbox label="Name">
          Name
        </el-checkbox>
        <el-checkbox label="Score">
          Score
        </el-checkbox>
      </el-checkbox-group>


      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-document" @click="handleDownload">
        导出Excel
      </el-button>
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
  const defaultFormThead = ['ID', 'Name', 'Score']

  export default {
    data() {
      return {
        downloadLoading: false,
        filename: '',
        autoWidth: true,
        bookType: 'xlsx',

        tableData: [],
        key: 1, // table key
        formTheadOptions: ['ID', 'Name', 'Score'],
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
          url: 'http://127.0.0.1:5000/store'
        }).then(response => {
          this.tableData = response.data
          console.log(response)
        });
      },


      handleDownload() {
        this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = this.formThead
          const filterVal = this.formThead
          const tableData = this.tableData
          const data = this.formatJson(filterVal, tableData)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: this.filename,
            autoWidth: this.autoWidth,
            bookType: this.bookType
          })
          this.downloadLoading = false
        })
      },
      formatJson(filterVal, jsonData) {
        return jsonData.map(v => filterVal.map(j => {
          if (j === 'timestamp') {
            return parseTime(v[j])
          } else {
            return v[j]
          }
        }))
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

