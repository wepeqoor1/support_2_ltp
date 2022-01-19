<template>
    <div>
        <div class="header-menu">
            <v-row>
                <v-col cols=3>
                    <v-row>
                        <v-text-field
                            v-model="user_inn"
                            label="ИНН"
                            clearable
                            clear-icon="close"/>
                        <v-btn
                            color="orange"  
                            @click=getSuperUserLoginPassword()>
                            <v-icon>search</v-icon>
                        </v-btn>
                        <v-col cols=1>
                            <v-btn 
                                x small
                                color="black"
                                @click=clearTable()
                                >
                                Очистить
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
              Номер контракта
            </th>
            <th>
              Пароль	
            </th>
            <th>
              Логин	
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in items"
            :key="item.name"
          >
            <td>{{ item.contract_id }}</td>
            <td>{{ item.user_password }}</td>
            <td>{{ item.user_login }}</td>
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
    <div v-if="show_error" class="red-text">Данного ИНН нет в базе данных</div>
    

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
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
            getSuperUserLoginPassword(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/super_user_login_password/" + this.user_inn, headers).then(
                response => this.processResponse(response))
            },
            clearTable(){
              this.show_error = false,
              this.items = []
            }
    }
}
</script>
