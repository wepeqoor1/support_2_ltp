<template>
    <div>
      <div class="header-menu">
          <v-row>
            <v-col cols=3>
              <v-row>
                <v-text-field
                    v-model="scratchcard"
                    label="Секретный код"
                    clearable
                    clear-icon="close"/>
                <v-btn
                    color="orange"
                    @click=getScratchcards()>
                    <v-icon>search</v-icon>
                </v-btn> 
              </v-row>
            </v-col>


            <v-col cols=3>
              <v-row>
                <v-text-field
                    v-model="scratchcard_number"
                    label="Номер карты"
                    clearable
                    clear-icon="close"/>

                <v-btn
                    color="orange"  
                    @click=getScratchcardsNumber()>
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
              Дата изменения статуса	
            </th>
            <th>
              Статус карты	
            </th>
            <th>
              Номер карты	
            </th>
            <th>
              Номинал	
            </th>
            <th>
              Контрагент	
            </th>
            <th>
              ИНН Контрагента	
            </th>
            <th>
              Клиент
            </th>
            <th>
              ИНН Клиента	
            </th>
            <th>
              Номер заявки
            </th>
            <th>
              РНМ ККТ
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in items"
            :key="item.name"
          >
            <td>{{ item.status_change_date }}</td>
            <td>{{ item.status }}</td>
            <td>{{ item.number }}</td>
            <td>{{ item.nominalvalue }}</td>
            <td>{{ item.contragent_sname }}</td>
            <td>{{ item.contragent_inn }}</td>
            <td>{{ item.client_sname }}</td>
            <td>{{ item.client_inn }}</td>
            <td>{{ item.request_id }}</td>
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
    <div v-if="show_error" class="red-text">Карты по указанному поисковому запросу не найдены. Измените поисковой запрос.</div>

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        scratchcard: "",
        scratchcard_number: "",
        items: [],
        show_error: false
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
            getScratchcards(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/scratchcard/" + this.scratchcard, headers).then(
                response => this.processResponse(response))
            },
            getScratchcardsNumber(){
              let headers = {headers: {Authorization: "Bearer " + this.$store.state.token}}
              axios.get(this.$store.state.host + "/api/users/scratchcard_number/" + this.scratchcard_number, headers).then(
                response => this.processResponse(response))
            },
            clearTable(){
              this.show_error = false,
              this.items = []
            }
    }
}
</script>

