<template>
  <div>
    <el-button
      class="filter-item"
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
        <br>
        <br>
        <el-checkbox
          v-model="choose_all_Organizations"
          @change="selectAll"
        >
          全选
        </el-checkbox>
      </div>

      <div slot="footer" class="dialog-footer">
<!--        <el-button @click="dialogFormVisible = false">取 消</el-button>-->
        <el-button type="primary" @click="Organization_confirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>

var Organizations = ['ARMY', 'NAVY', 'AF', 'DEFW', 'DHA', 'DISA', 'DLA', 'DODEA', 'DTRA', 'MDA', 'NGA', 'NSA', 'SOCOM', 'TJS', 'DIA', 'WHS', 'TMA', 'DFAS', 'DAU', 'CMP', 'DCAA', 'DCMA', 'DCSA', 'DHRA', 'DLSA', 'DMACT', 'DPAA', 'DSCA', 'DTIC', 'DTSA', 'OEA', 'OSD', 'SDA', 'IG', 'CAAF', 'DEPS', 'DEPSDDR', 'DSS', 'NDU', 'DPMO', 'DHP', 'DEFR', 'BTA', 'CBDP', 'DARPA', 'OTE', 'TRANSCOM', 'DECA']

export default {
  data () {
    return {
      Organizations: Organizations,
      Organizations_selected: Organizations,
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
