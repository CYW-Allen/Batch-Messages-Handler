<template>
  <div v-if="appStatus.mailFile === null" class="fit uploadArea relative-position">
    <div class="fit text-h3 text-bold uploadAreaLabel row justify-center items-center">Click here to import file</div>
    <q-file class="fit uploadComp" input-class="text-h3 text-bold" borderless v-model="appStatus.mailFile" accept=".csv"
      @rejected="$q.notify({ message: 'Invalid file format' })" />
  </div>

  <q-table v-else ref="mailTable" class="fit stickyHeader" :title="tableTitle" :columns="tableCols"
    :rows="listAll ? appStatus.mails : appStatus.selectedRows" row-key="Index" virtual-scroll
    :pagination="{ rowsPerPage: 0 }" :rows-per-page-options="[0]" hide-bottom selection="multiple"
    :virtual-scroll-sticky-size-start="48" v-model:selected="appStatus.selectedRows" :filter="filter">
    <template v-slot:top-right>
      <toggle-btn class="q-mr-md" :ele-id="'viewMode'" :vals="{ left: 'All', right: 'Selected' }"
        @status-change="changeTableContent" />
      <q-input dense debounce="300" v-model="filter" placeholder="Search..." />
      <q-input class="q-ml-md" dense v-model="replace" placeholder="Replace to...">
        <template v-slot:append>
          <q-icon class="cursor-pointer" name="fa-solid fa-rotate" title="replace" @click="replaceStr" />
        </template>
      </q-input>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td>
          <q-checkbox v-model="props.selected" @click="selectRow($event, props.rowIndex)"></q-checkbox>
        </q-td>
        <q-td v-for="col in tableCols" :key="col.name" :props="props">
          <div v-if="col.name === 'Index'" class="text-center">{{ props.row.Index }}</div>
          <div v-else class="ellipsis" style="max-width: 600px;">{{ props.row[col.name] }}</div>
          <q-popup-edit v-if="col.name !== 'Index'" v-model="props.row[col.name]" v-slot="scope"
            :title="`Modify row ${props.rowIndex + 1}, column ${col.name}`" :validate="(val) => val !== ''" buttons
            label-set="Confirm" label-cancel="Cancel">
            <q-input type="textarea" v-model="scope.value" autofocus
              :rules="[(val) => val.length > 0 || '⚠ The value must not be empty']" />
          </q-popup-edit>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import papa from 'papaparse';
import dayjs from 'dayjs';
import { useAppStatusStore } from 'src/stores/appStatus';
import ToggleBtn from './ToggleBtn.vue';

const $q = useQuasar();
const appStatus = useAppStatusStore();

const mailTable = ref(null);
const tableTitle = computed(() => (appStatus.mailFile ? appStatus.mailFile.name.split('.csv')[0] : ''));
const tableCols = computed(() => (
  Object.keys(appStatus.mails[0] || {})
    .map((col) => ({
      name: col,
      label: col,
      field: (row) => row[col],
      sortable: false,
      align: 'left',
      style: 'font-size: 1rem',
    }))
));
const listAll = ref(true);
const filter = ref('');
const replace = ref('');

function changeTableContent(val) {
  listAll.value = val;
}

function replaceStr() {
  if (filter.value !== '' && replace.value !== '') {
    const newContent = JSON.stringify(appStatus.mails)
      .replaceAll(
        filter.value.replaceAll('\\', '\\\\'),
        replace.value === '\\n' ? '\\\\n' : replace.value,
      );
    appStatus.mails = JSON.parse(newContent);
    filter.value = '';
  }
}

function selectRow(event, curSelectedIndex) {
  if (event.shiftKey && appStatus.selectedRows.length > 1) {
    const previousSelectedIndex = appStatus.selectedRows[appStatus.selectedRows.length - 2].Index - 1;
    const rangeStart = Math.min(curSelectedIndex, previousSelectedIndex);
    const rangeEnd = Math.max(curSelectedIndex, previousSelectedIndex);

    appStatus.selectedRows = appStatus.mails.slice(rangeStart, rangeEnd + 1);
  }
}

watch(() => appStatus.mailFile, (v) => {
  if (v) {
    const fileReader = new FileReader();

    fileReader.addEventListener('load', () => {
      appStatus.mails = papa.parse(fileReader.result, { header: true, skipEmptyLines: true })
        .data.map((row, i) => ({ Index: i + 1, ...row }));

      const defaultPublicTimeStr = dayjs().add(appStatus.mails.length, 'second').format('YYYY/MM/DD HH:mm:ss');

      appStatus.defaultPublicTime = defaultPublicTimeStr;
      appStatus.publicTime = defaultPublicTimeStr;
    });
    fileReader.readAsText(appStatus.mailFile);
  }
});

watch(() => appStatus.mails, (v) => {
  console.log('mails: ', v);
});

watch(mailTable, (v) => {
  if (v) appStatus.mailTableRef = v;
});

watch(() => appStatus.selectedRows, (v) => {
  console.log('selected rows:', v);
});
</script>

<style>
.uploadArea {
  border: none !important;
  background: linear-gradient(90deg, gray 50%, transparent 50%),
    linear-gradient(90deg, gray 50%, transparent 50%),
    linear-gradient(0deg, gray 50%, transparent 50%),
    linear-gradient(0deg, gray 50%, transparent 50%);
  background-repeat: repeat-x, repeat-x, repeat-y, repeat-y;
  background-size: 15px 5px, 15px 5px, 5px 15px, 5px 15px;
  background-position: 0 0, 0 100%, 0 0, 100% 0;
  animation: borderAnime 15s linear infinite;
}

@keyframes borderAnime {
  100% {
    background-position: 100% 0, -100% 100%, 0 -300%, 100% 300%;
  }
}

.uploadAreaLabel {
  position: absolute;
  top: 0;
  left: 0;
}

.uploadComp .q-field__control {
  height: 100%;
}

.stickyHeader .q-table__top {
  background-color: lightskyblue;
}

.stickyHeader thead tr th {
  position: sticky;
  z-index: 1;
  font-size: 1.2rem;
  font-weight: bold;
  background-color: lightcyan;
}

.stickyHeader thead tr:last-child th {
  top: 48px;
}

.stickyHeader thead tr:first-child th {
  top: 0;
}
</style>
