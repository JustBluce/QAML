<template>
  <div class="app-container">
    <div class="filter-container">

<!--      <el-input-->
<!--        v-model="listQuery.From"-->
<!--        placeholder="From"-->
<!--        style="width: 200px"-->
<!--        class="filter-item"-->
<!--        @keyup.enter.native="SearchData"-->
<!--      />-->
      <el-select
        v-model="listQuery.From"
        placeholder="From"
        clearable
        style="width: 90px"
        class="filter-item"
      >
        <el-option
          v-for="item in FromOptions"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>

      <el-select
        v-model="listQuery.Year"
        placeholder="Year"
        clearable
        style="width: 90px"
        class="filter-item"
      >
        <el-option
          v-for="item in YearOptions"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>

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
        @click="SearchData"
      >
        Search
      </el-button>

      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-document" @click="handleDownload">
        导出Excel
      </el-button>
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox label="ID">
          ID
        </el-checkbox>
        <el-checkbox label="From">
          From
        </el-checkbox>
        <el-checkbox label="Account_Title">
          Account_Title
        </el-checkbox>
        <el-checkbox label="Year">
          Year
        </el-checkbox>
        <el-checkbox label="Budget_Activity_Title">
          Budget_Activity_Title
        </el-checkbox>
        <el-checkbox label="Organization">
          Organization
        </el-checkbox>
        <el-checkbox label="TOA_Amount">
          TOA_Amount
        </el-checkbox>

      </el-checkbox-group>

    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      border
      fit
      highlight-current-row
      style="width: 100%"
      @sort-change="sortChange"
    >
      <el-table-column v-for="ID in formThead" :key="ID" :label="ID">
        <template slot-scope="scope">
          {{ scope.row[ID] }}
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />



    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5, 10, 20, 40]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="list.length">
    </el-pagination>

  </div>
</template>

<script>
import {
  fetchList,
  fetchPv,
  createArticle,
  updateArticle,
} from "@/api/article";
import waves from "@/directive/waves"; // waves directive
import { parseTime } from "@/utils";
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: "CN", display_name: "China" },
  { key: "US", display_name: "USA" },
  { key: "JP", display_name: "Japan" },
  { key: "EU", display_name: "Eurozone" },
];

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name;
  return acc;
}, {});

const defaultFormThead = ["ID", "From", "Budget_Activity_Title", "Account_Title", "Year", "Organization", "TOA_Amount"]

export default {
  name: "ComplexTable",
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: "success",
        draft: "info",
        deleted: "danger",
      };
      return statusMap[status];
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type];
    },
  },
  data() {
    return {

      //这段是用于选择显示哪个表头的
      key: 1, // table key
      formTheadOptions: defaultFormThead,
      checkboxVal: defaultFormThead, // checkboxVal
      formThead: defaultFormThead, // 默认表头 Default header

      //这段是用于下载xlsx文件的
      filename: '',
      autoWidth: true,
      bookType: 'xlsx',
      tableData:[],
      //这段是用于翻页的
      currentPage:1,
      pagesize:10,
      userList: [],

      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,

      listQuery: {
        From: undefined,
        Year: undefined,
        Organization:  undefined,
      },
      importanceOptions: [1, 2, 3],
      FromOptions: ["c1", "m1","o1","p1","p1r","r1","rf1"],
      YearOptions: ["2021", "2020","2019","2018","2017","2016","2015","2014","2013"],
      OrganizationOptions: ['ARMY', 'NAVY', 'AF', 'DEFW', 'DHA', 'DISA', 'DLA', 'DODEA', 'DTRA', 'MDA', 'NGA', 'NSA', 'SOCOM', 'TJS', 'DIA', 'WHS', 'TMA', 'DFAS', 'DAU', 'CMP', 'DCAA', 'DCMA', 'DCSA', 'DHRA', 'DLSA', 'DMACT', 'DPAA', 'DSCA', 'DTIC', 'DTSA', 'OEA', 'OSD', 'SDA', 'IG', 'CAAF', 'DEPS', 'DEPSDDR', 'DSS', 'NDU', 'DPMO', 'DHP', 'DEFR', 'BTA', 'CBDP', 'DARPA', 'OTE', 'TRANSCOM', 'DECA'],
      calendarTypeOptions,
      sortOptions: [
        { label: "ID Ascending", key: "+id" },
        { label: "ID Descending", key: "-id" },
      ],
      statusOptions: ["published", "draft", "deleted"],
      showReviewer: false,

      temp: {
        id: undefined,
        From: "",
        Budget_Activity_Title: "",
        Account_Title: "",
        Year: "",
        Organization: "",
        TOA_Amount: "",
      },

      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "Edit",
        create: "Create",
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [
          { required: true, message: "type is required", trigger: "change" },
        ],
        timestamp: [
          {
            type: "date",
            required: true,
            message: "timestamp is required",
            trigger: "change",
          },
        ],
        title: [
          { required: true, message: "title is required", trigger: "blur" },
        ],
      },
      downloadLoading: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    handleSizeChange: function (size) {
      this.pagesize = size;
      console.log(this.pagesize)  //每页下拉显示数据
    },
    handleCurrentChange: function(currentPage){
      this.currentPage = currentPage;
      console.log(this.currentPage)  //点击第几页
    },

    getList() {
      this.listLoading = true;
      fetchList(this.listQuery).then((response) => {
        this.list = response.data.items;
        this.total = response.data.total;

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 10000);
      });
    },

    fetchData: function () {
      this.listLoading = true;
      this.axios({
        method: "GET",
        url: "http://127.0.0.1:5000/show/get",
      }).then((response) => {
        this.list = response.data;
        // this.total = response.data.total
        console.log(response);
      });
      this.listLoading = false;
    },

    SearchData: function () {
      this.listLoading = true;

      let formData = new FormData();
      formData.append("From", this.listQuery.From);
      formData.append("Year", this.listQuery.Year);
      formData.append("Organization", this.listQuery.Organization);

      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/show/search",
        data: formData,
      }).then((response) => {
        this.list = response.data;
        // this.total = response.data.total
        console.log(response);
      });
      this.listLoading = false;
    },


    handleFilter() {
      this.listQuery.page = 1;
      this.getList();
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: "操作Success",
        type: "success",
      });
      row.status = status;
    },
    sortChange(data) {
      const { prop, order } = data;
      if (prop === "ID") {
        this.sortByID(order);
      }
    },
    sortByID(order) {
      if (order === "ascending") {
        this.listQuery.sort = "+ID";
      } else {
        this.listQuery.sort = "-ID";
      }
      this.handleFilter();
    },
    resetTemp() {
      this.temp = {

        ID: undefined,
        Year: "",
        From: "",
        // Account_Title: "",
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },



    //这段用于下载excel
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
    formatJson(filterVal) {
      return this.list.map((v) =>
        filterVal.map((j) => {
          if (j === "timestamp") {
            return parseTime(v[j]);
          } else {
            return v[j];
          }
        })
      );
    },
  },
  watch: {
    checkboxVal(valArr) {
      this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
      this.key = this.key + 1// 为了保证table 每次都会重渲 In order to ensure the table will be re-rendered each time
    }
  }

};
</script>
