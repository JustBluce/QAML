<template>
  <div>
    <!-- v-if="showall" class="app-container" -->
    <!-- <div>
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox label="ID"> ID </el-checkbox>
        <el-checkbox label="From"> From </el-checkbox>
        <el-checkbox label="Account_Title"> Account_Title </el-checkbox>
        <el-checkbox label="Year"> Year </el-checkbox>
      </el-checkbox-group>
    </div> -->

<!-- v-loading="listLoading" -->
    <el-table
      :key="tableKey"
      :data="list.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
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

    <!-- <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />

    <el-pagination
      :current-page="currentPage"
      :page-sizes="[5, 10, 20, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="list.length"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    /> -->
  </div>
</template>

<script>
import { fetchList } from "@/api/article";
import waves from "@/directive/waves"; // waves directive
import { parseTime } from "@/utils";
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination
import Select_org from "./components/Select_org";
import Select_from from "./components/Select_from";

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

const defaultFormThead = ["ID", "Username", "Email", "Score", "LastLogin"];

export default {
  name: "ComplexTable",
  components: {
    Pagination,
    Select_org,
    Select_from,
  },
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
      defaultYear: [],
      defaultOrganization: [],
      defaultFrom: [],

      showall: false,

      // 这段是用于选择显示哪个表头的
      key: 1, // table key
      formTheadOptions: defaultFormThead,
      checkboxVal: defaultFormThead, // checkboxVal
      formThead: defaultFormThead, // 默认表头 Default header

      // 这段是用于下载xlsx文件的
      filename: "",
      autoWidth: true,
      bookType: "xlsx",
      tableData: [],
      // 这段是用于翻页的
      currentPage: 1,
      pagesize: 20,
      userList: [],

      tableKey: 0,
      list: [
        {
          ID: "1",
          Username: "Michael Hiller",
          Email: "MichHill@gmail.com",
          Score: 97,
          LastLogin: "2021-07-26 14:32:22",
        },
        {
          ID: "2",
          Username: "Ashley",
          Email: "MichHill@gmail.com",
          Score: 84,
          LastLogin: "2021-07-26 14:32:22",
        },
        {
          ID: "3",
          Username: "Magret",
          Email: "MichHill@gmail.com",
          Score: 75,
          LastLogin: "2021-07-26 14:32:22",
        },
        {
          ID: "4",
          Username: "Simon",
          Email: "MichHill@gmail.com",
          Score: 64,
          LastLogin: "2021-07-26 14:32:22",
        },
        {
          ID: "5",
          Username: "Godman",
          Email: "MichHill@gmail.com",
          Score: 52,
          LastLogin: "2021-07-26 14:32:22",
        },
        {
          ID: "6",
          Username: "Balcon",
          Email: "MichHill@gmail.com",
          Score: 44,
          LastLogin: "2021-07-26 14:32:22",
        },
      ],
      total: 0,
      listLoading: true,

      SearchData_Year: {
        FromYear: "",
        ToYear: "",
      },

      listQuery: {
        From: [],
        Year: [],
        Organization: [],
      },
      importanceOptions: [1, 2, 3],
      FromOptions: [],
      YearOptions: [],
      OrganizationOptions: [],
      calendarTypeOptions,
      sortOptions: [
        { label: "ID Ascending", key: "+id" },
        { label: "ID Descending", key: "-id" },
      ],
      statusOptions: ["published", "draft", "deleted"],
      showReviewer: false,

      temp: {
        name: "Michael Hiller",
        email: "MichHill@gmail.com",
        Score: 97,
        LastLogin: "2021-07-26 14:32:22",
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
  watch: {
    showall: function () {
      this.$nextTick(function () {
        this.fetchData();
      });
    },
    checkboxVal(valArr) {
      this.formThead = this.formTheadOptions.filter(
        (i) => valArr.indexOf(i) >= 0
      );
      this.key = this.key + 1; // 为了保证table 每次都会重渲 In order to ensure the table will be re-rendered each time
    },
  },

  created() {
    this.start_initialize();
  },
  mounted() {},
  methods: {
    async start_initialize() {
      await this.axios({
        method: "GET",
        url: "http://127.0.0.1:5000/initialize/summarize",
      }).then((response) => {
        const data = response.data;
        // this.defaultYear = data["year"];
        // this.defaultOrganization = data["Organization"];
        // this.defaultFrom = data["from"];
        console.log("初始化完成");
        this.showall = true;
      });
    },
    child_to_org(data) {
      this.listQuery.Organization = data;
      console.log(this.listQuery.Organization);
    },
    child_to_from(data) {
      this.listQuery.From = data;
      console.log(this.listQuery.From);
    },
    handleSizeChange: function (size) {
      this.pagesize = size;
      console.log(this.pagesize); // 每页下拉显示数据
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      console.log(this.currentPage); // 点击第几页
    },

    getList() {
      this.listLoading = true;
      fetchList(this.listQuery).then((response) => {
        // this.list = response.data.items
        // this.total = response.data.total
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
        // this.list = response.data
        console.log(response);
      });
      this.listLoading = false;
    },

    SearchData: function () {
      this.listLoading = true;

      const formData = new FormData();
      formData.append("From", this.listQuery.From);
      formData.append("Year", this.listQuery.Year);
      formData.append("Organization", this.listQuery.Organization);

      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/show/search",
        data: formData,
      }).then((response) => {
        this.list = response.data;
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
};
</script>

<style>
.radio-label {
  font-size: 14px;
  color: #606266;
  line-height: 40px;
  padding: 0 12px 0 30px;
}
.ldstest {
  font-size: 14px;
  color: #666666;
  line-height: 40px;
  padding: 0 10px 0 10px;
}
.chart-wrapper {
  background: #f9ffff;
  padding: 3px 0px;
  margin-bottom: 0;
}
</style>
