<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">Login Form</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">Login</el-button>

      <el-button style="width:100%;margin-bottom:30px;"  @click="dialogFormVisible1 = true">Register account</el-button>
      <el-button style="width:100%;margin-bottom:30px;"  @click="dialogFormVisible2 = true">Change password</el-button>




      <el-dialog title="Register  account" :visible.sync="dialogFormVisible1"  >
<!--        rules是传入规则，验证，下方其实没有规则传入-->
        <div>
          <el-form :model="addForm" label-width="80px">
            <el-form-item label="Username:">
              <el-input v-model.trim="addForm.username" aria-placeholder="Please enter username" clearable></el-input>
            </el-form-item>
            <el-form-item label="Password:">
              <el-input v-model.trim="addForm.password" aria-placeholder="Please enter password" clearable></el-input>
            </el-form-item>
          </el-form>
          <el-button @click="dialogFormVisible1 = false">Cancel</el-button>
          <el-button type="primary" @click="From_confirm1">Confirm</el-button>
        </div>
      </el-dialog>
      <el-dialog title="Change password" :visible.sync="dialogFormVisible2"  >
        <!--        rules是传入规则，验证，下方其实没有规则传入-->
        <div>
          <el-form :model="changeForm" label-width="80px">
            <el-form-item label="Username:">
              <el-input v-model.trim="changeForm.username" aria-placeholder="Please enter username" clearable></el-input>
            </el-form-item>
            <el-form-item label="Old password:">
              <el-input v-model.trim="changeForm.password_old" aria-placeholder="Please enter old password" clearable></el-input>
            </el-form-item>
            <el-form-item label="New password:">
              <el-input v-model.trim="changeForm.password_new" aria-placeholder="Please enter new password" clearable></el-input>
            </el-form-item>
          </el-form>
          <el-button @click="dialogFormVisible2 = false">Cancel</el-button>
          <el-button type="primary" @click="From_confirm2">Confirm</el-button>
        </div>
      </el-dialog>
      <!-- <div class="tips">
        <span style="margin-right:20px;">Default Account Number： lds</span>
        <span> Default Password： lds12321</span>
      </div> -->

    </el-form>
  </div>
</template>

<script>
// import { validUsername } from '@/utils/validate'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!this.Username_False) {
        callback(new Error('Username does not exist'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 0) {
        callback(new Error('Password length should be greater than 0 digits'))
      } else if (!this.Password_False) {
        callback(new Error('Your password was entered incorrectly'))
      } else {
        callback()
      }
    }
    return {
      addForm: {
        username: '',
        password: ''
      },
      loginForm: {
        username: 'lds',
        password: 'lds12321'
      },
      changeForm: {
        username: '',
        password_old: '',
        password_new: ''
      },
      Username_False:false,
      Password_False:false,
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      dialogFormVisible1: false,
      dialogFormVisible2: false
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    From_confirm1(){
      let formData = new FormData();
      formData.append("User", this.addForm.username);
      formData.append("Password", this.addForm.password);

      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/log/add",
        data:formData,
      }).then((response) => {
        console.log(response.data);
        if (response.data=='Successfully add new user'){
          this.$message.success('Successfully add new user')
          this.dialogFormVisible1 = false;
        }else {
          this.$message.error('The user already exists')
        }
      });
    },
    From_confirm2(){
      let formData = new FormData();
      formData.append("User", this.changeForm.username);
      formData.append("Password_old", this.changeForm.password_old);
      formData.append("Password_new", this.changeForm.password_new);

      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/log/change",
        data:formData,
      }).then((response) => {
        console.log(response.data);
        if (response.data=='Successfully changed'){
          this.$message.success(response.data)
          this.dialogFormVisible2 = false;
        }else if(response.data=='Password input error, change failed'){
          this.$message.error(response.data)
        }else if(response.data=='User does not exist'){
          this.$message.error(response.data)
        }else {
          this.$message.error('Unknown error')
        }
      });
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      let formData = new FormData();
      formData.append("User", this.loginForm.username);
      formData.append("Password", this.loginForm.password);

      this.axios({
        method: "POST",
        url: "http://127.0.0.1:5000/log/in",
        data: formData,
      }).then((response) => {
        console.log(response.data);
        if (response.data=='User does not exist'){
          this.Username_False=false
          this.Username_False=true
        }
        if (response.data=='Incorrect password'){
          this.Username_False=true
          this.Password_False=false
        }
        if (response.data=='Correct password'){
          this.Username_False=true
          this.Password_False=true
          // this.$refs.loginForm.validate(valid => {
          //   if (valid) {
          //     this.loading = true
          //     this.$store.dispatch('user/login', this.loginForm).then(() => {
          //       this.$router.push({ path: this.redirect || '/' })
          //       this.loading = false
          //     }).catch(() => {
          //       this.loading = false
          //     })
          //   } else {
          //     console.log('error submit!!')
          //     return false
          //   }
          // })
          this.$refs.loginForm.validate(valid => {
            if (valid) {
              this.loading = true
              this.$store.dispatch('user/login', this.loginForm).then(() => {
                this.$router.push({ path: this.redirect || '/' })
                this.loading = false
              }).catch(() => {
                this.loading = false
              })
            } else {
              console.log('error submit!!')
              return false
            }
          })
        }
      });
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
