<template>
    <div>
      <div class="header-menu">
        <v-row>
          <v-col cols=3>
            <v-row>
              <v-text-field
                  v-model="user_mail"
                  label="Email"
                  clearable
                  clear-icon="close"/>
              <v-btn
                  color="orange"
                  @click=getForUserMail()>
                  <v-icon>search</v-icon>
              </v-btn> 
            </v-row>
          </v-col>

          <v-col cols=3>
            <v-row>
              <v-text-field
                  v-model="user_inn"
                  label="ИНН"
                  clearable
                  clear-icon="close"/>

              <v-btn
                  color="orange"  
                  @click=getForUserInn()>
                  <v-icon>search</v-icon>
              </v-btn> 
              
              <v-col cols=2>
                <v-btn 
                  block
                  x small
                  color="black"
                  @click=getCountQueueCompany()
                >
                Очередь на выгрузку
                </v-btn>
              </v-col>
              
            </v-row>
            
          </v-col>
        </v-row>
      </div>

    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th>
              Наименование компании	
            </th>
            <th>
              ИНН	
            </th>
            <th>
              Почта	
            </th>
            <th>
              Кол-во касс	
            </th>
            <th>
              Начало периода выгрузки	
            </th>
            <th>
              Конец периода выгрузки	
            </th>
            <th>
              Начало выполнения выгрузки
            </th>
            <th>
              Конец выполнения выгрузки	
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in items"
            :key="item.name"
          >
            <td>{{ item.company_caption }}</td>
            <td>{{ item.company_inn }}</td>
            <td>{{ item.user_mail }}</td>
            <td>{{ item.kkts }}</td>
            <td>{{ item.period_stat_start }}</td>
            <td>{{ item.period_stat_end }}</td>
            <td>{{ item.time_request }}</td>
            <td>{{ item.time_finish }}</td>
            <td>
              <div v-for="item in item.items" :key=item>
                {{ item }}
              </div>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <div/>
    <div v-if="show_error" class="red-text">В данный момент выгрузок нет</div>
    

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        user_mail: "",
        user_inn: "",
        items: [],
        show_error: false,
      }
    },
    methods:{
            processResponse(response){
                    this.items = response.data
                    if (this.items.length == 0){
                      this.show_error = true
                    }
                    else {
                      this.show_error = false
                    } 
            },
            getForUserMail(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/stat_fiscal_doc_sender_queue/user_mail/" + this.user_mail, headers).then(
                response => this.processResponse(response))
            },
            getForUserInn(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/stat_fiscal_doc_sender_queue/user_inn/" + this.user_inn, headers).then(
                response => this.processResponse(response))
            },
            getCountQueueCompany(){
                let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/stat_fiscal_doc_sender_queue/", headers).then(
                response => this.processResponse(response))
            },
            clearTable(){
              this.show_error = false,
              this.items = []
            }
    }
}
</script>
