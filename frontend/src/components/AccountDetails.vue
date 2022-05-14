<template>
  <div class="q-pa-md">
    <q-virtual-scroll
      type="table"
      style="max-height: 70vh"
      :virtual-scroll-item-size="48"
      :virtual-scroll-sticky-size-start="48"
      :virtual-scroll-sticky-size-end="32"
      :items="transactions"
    >
      <template v-slot:before>
        <thead class="thead-sticky text-left">
          <tr>
            <th>Index</th>
            <th v-for="col in columns" :key="'1--' + col.name">
              {{ col }}
            </th>
          </tr>
        </thead>
      </template>
      <template v-slot="{ item: row, index }">
        <tr :key="index">
          <td>#{{ index+1 }}</td>
          <td v-for="col in columns" :key="index + '-' + col">
            {{ getFormattedData(row[col], col) }}
          </td>
        </tr>
      </template>
    </q-virtual-scroll>
  </div>
</template>

<script>

import { mapActions, mapGetters } from "vuex";

export default {
  name: 'AccountDetails',
  data() {
    return {
      transactions: [],
      columns: [
        'transaction_id',
        'status',
        'type',
        'reason',
        'transaction_from',
        'transaction_to',
        'amount'
      ]
    }
  },
  computed: {
    ...mapGetters('Account', ['getTransactionsData'])
  },
  methods: {
    ...mapActions('Account', ['getTransactions', 'getTransactionsWithFilter']),
    getFormattedData(row, col_name) {
      let row_entry = null;
      switch (col_name) {
        case 'transaction_from':
          row_entry = this.getFormattedName(row.user.first_name, row.user.last_name);
          break;
        case 'transaction_to':
          row_entry = this.getFormattedName(row.user.first_name, row.user.last_name);
          break;
        default:
          row_entry = row
          break;
      }
      return row_entry
    },
    getFormattedName(first_name, last_name) {
      return first_name + ' ' + last_name
    },
  },
  async mounted() {
    await this.getTransactions();
    this.transactions = this.getTransactionsData
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="sass">
.thead-sticky tr > *,
.tfoot-sticky tr > *
  position: sticky
  opacity: 1
  z-index: 1
  background: black
  color: white

.thead-sticky tr:last-child > *
  top: 0

.tfoot-sticky tr:first-child > *
  bottom: 0
</style>
