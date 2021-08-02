<template>
  <div>
    <el-button
      @click="dialogFormVisible = true"
    >
      选择组织
    </el-button>
    <el-dialog title="选择组织" :visible.sync="dialogFormVisible"  @closed="handleClose">
      <div>
        <el-checkbox
          v-for="org in Organizations"
          v-model="Organizations_selected"
          :label="org">
          {{org}}
        </el-checkbox>
        <el-checkbox
          v-model="choose_all_Organizations"
          @change="selectAll"
        >
          全选
        </el-checkbox>
      </div>

      <div slot="footer" class="dialog-footer">
<!--        <el-button @click="dialogFormVisible = false">取 消</el-button>-->
        <el-button  @click="Organization_confirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>


export default {
  props:['Organizations','Organizations_selected'],
  data() {
    return {
      choose_all_Organizations:true,
      dialogFormVisible: false,
    }
  },

  methods: {
    // handleClose() {
    //   this.$refs.ruleForm.resetFields()
    // },
    selectAll() {
      var _this = this;
      if (!this.choose_all_Organizations) {
        this.Organizations_selected = [];
      } else {
        _this.Organizations_selected = [];
        _this.Organizations.forEach(function(org) {
          _this.Organizations_selected.push(org);
        });
      }
    },
    Organization_confirm(){
      this.dialogFormVisible = false;
      this.$emit('child-event',this.Organizations_selected);
    }
  }
}
</script>

<style lang="less" scoped>

</style>
