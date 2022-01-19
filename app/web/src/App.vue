<template>
  <div id="app">
      <div v-if='$store.state.token'>    
        <v-tabs
          background-color="deep-purple accent-4"
          center-active
          dark
        >
          <v-tab 
            @click='page=1'
            >
            Скретч-карты
          </v-tab>
          
          <v-tab 
            @click='page=2'
            >
            Выгрузка
          </v-tab>

          <v-tab 
            @click='page=3'
            >
            ККТ
          </v-tab>          

          <v-tab 
            @click='page=4'
            >
            Супер-пользователь
          </v-tab>  
      
          <v-spacer></v-spacer>
                    v.0.2.3

          <v-btn align-end 
                 color="orange"  
                 @click=logout()>
                 Выйти
          </v-btn> 

        </v-tabs>
        <TablePage v-if='page == 1'/>
        <StatFiscalSendQue v-if='page == 2'/>
        <Kkt v-if='page == 3'/>
        <SuperUserLoginPassword v-if='page == 4'/>
      </div>
      <LoginPage v-else/>
  </div>
</template>


<script>
import LoginPage from './components/LoginPage.vue'
import TablePage from './components/TablePage.vue'
import StatFiscalSendQue from './components/StatFiscalSendQue.vue'
import Kkt from './components/Kkt.vue'
import SuperUserLoginPassword from './components/SuperUserLoginPassword.vue'

export default {
  name: 'App',
  components: {
    LoginPage,
    TablePage,
    StatFiscalSendQue,
    Kkt,
    SuperUserLoginPassword
    },
    data (){
      return {
        page: 1
      }
    },
    methods:{
            logout(){
                localStorage.removeItem('token')
                this.$store.state.token = null
            }
        }
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.header-menu {
  margin-left: 60px;

}
.red-text{
    color: red;
  }
</style>
