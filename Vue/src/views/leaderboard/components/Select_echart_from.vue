<template>
  <div>
    <el-button
      @click="dialogFormVisible = true"
    >
      选择预算类型
    </el-button>
    <el-dialog title="选择预算类型" :visible.sync="dialogFormVisible"  >
      <div>
        <el-checkbox
          v-for="org in From"
          v-model="From_selected"
          :label="org">
          {{org}}
        </el-checkbox>
        <el-checkbox
          v-model="choose_all_From"
          @change="selectAll"
        >
          全选
        </el-checkbox>
      </div>

      <div slot="footer" class="dialog-footer">
<!--        <el-button @click="dialogFormVisible = false">取 消</el-button>-->
        <el-button type="primary" @click="From_confirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>


export default {
  props:['From','From_selected'],
  data() {
    return {
      choose_all_From:true,
      dialogFormVisible: false,
    }
  },

  methods: {
    selectAll() {
      var _this = this;
      if (!this.choose_all_From) {
        this.From_selected = [];
      } else {
        _this.From_selected = [];
        _this.From.forEach(function(org) {
          _this.From_selected.push(org);
        });
      }
    },
    From_confirm(){
      this.dialogFormVisible = false;
      this.$emit('child-event',this.From_selected);
    }
  }
}
</script>

<style lang="less" scoped>

</style>

