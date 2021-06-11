<template>
  <div>
  <el-table
    :data="tableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
    style="width: 100%">
    <el-table-column
      label="日期"
      width="180">
      <template slot-scope="scope">
        <i class="el-icon-time"></i>
        <span style="margin-left: 10px">{{ scope.row.date }}</span>
      </template>
    </el-table-column>
    <el-table-column
      label="姓名"
      width="180">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top">
          <p>姓名: {{ scope.row.name }}</p>
          <p>住址: {{ scope.row.address }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag size="medium">{{ scope.row.name }}</el-tag>
          </div>
        </el-popover>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">aa</el-button>
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-sizes="[5, 10, 20, 40]"
    :page-size="pagesize"
    layout="total, sizes, prev, pager, next, jumper"
    :total="tableData.length">
  </el-pagination>
  <p>{{tableData}}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [{
        'date': '2016-05-02',
        'name': 'sasas',
        'address': '上海市普陀区金沙江路 1518 弄'
      }, {
        'date': '2016-05-04',
        'name': '王小虎',
        'address': '上海市普陀区金沙江路 1517 弄'
      }, {
        'date': '2016-05-01',
        'name': '王小虎',
        'address': '上海市普陀区金沙江路 1519 弄'
      }, {
        'date': '2016-05-03',
        'name': '王小虎',
        'address': '上海市普陀区金沙江路 1516 弄'
      }]
      ,
      currentPage:1,
      pagesize:3,
      userList: []
    }
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    }
    //下面一串代码是关于分页的
    ,
    handleSizeChange: function (size) {
      this.pagesize = size;
      console.log(this.pagesize)  //每页下拉显示数据
    },
    handleCurrentChange: function(currentPage){
      this.currentPage = currentPage;
      console.log(this.currentPage)  //点击第几页
    },
    handleUserList() {
      this.axios.get('http://127.0.0.1:5000/toeletry1').then(response => {
        this.tableData=response.data  //tableData最后要转成的形式：[ { "date": "2016-05-02", "name": "王小虎", "address": "上海市普陀区金沙江路 1518 弄" }, { "date": "2016-05-04", "name": "王小虎", "address": "上海市普陀区金沙江路 1517 弄" } ]
        console.log(response);//这里可以打印出我想要的数据
      }).catch((err) => {
        console.log(err);
      });
    }
  },
  created() {
    this.handleUserList()
  }
}
</script>
