<template>
  <q-card class="fit column">
    <q-card-section class="col">
      <q-scroll-area class="fit">
        <q-list bordered class="rounded-borders">
          <q-expansion-item expand-separator group="cfg" class="text-h6" icon="fa-regular fa-pen-to-square"
            label="Modify content">
            <template v-slot:header>
              <q-item-section avatar>
                <q-icon name="fa-regular fa-pen-to-square" />
              </q-item-section>
              <q-item-section>
                <div>Modify content</div>
              </q-item-section>
              <q-badge color="red" class="q-mr-md">{{ `Selected: ${appStatus.selectedRows.length}` }}</q-badge>
            </template>
            <div class="q-pa-md">
              <q-btn-group v-if="appStatus.mails.length" glossy push class="q-mb-sm">
                <q-btn label="Edit col" color="light-blue-8" no-caps @click="appStatus.displayModifyColDlg = true" />
                <q-btn label="Edit row" color="green-8" no-caps @click="appStatus.displayModifyRowDlg = true" />
              </q-btn-group>

              <q-input type="textarea" v-for="col, i in cols" :key="i" class="text-h6" filled square
                :bg-color="`indigo-${1 + (i % 2)}`" v-model="newValueInCol[col]">
                <template v-slot:prepend>
                  <div class="text-bold">{{ `${col} : ` }}</div>
                </template>
                <template v-slot:append>
                  <q-btn v-if="newValueInCol[col]?.length" round push glossy color="grey-8" icon="fa-solid fa-eraser"
                    title="Clear" @click="newValueInCol[col] = ''" />
                  <q-btn v-if="appStatus.selectedRows.length" round push glossy color="primary q-ml-sm"
                    icon="fa-solid fa-pen" title="Apply" @click="batchModCont(col, newValueInCol[col])"
                    :disable="!newValueInCol[col] || newValueInCol[col].length === 0" />
                </template>
              </q-input>
            </div>
          </q-expansion-item>

          <q-expansion-item ref="timeCfg" expand-separator group="cfg" class="text-h6" icon="fa-regular fa-clock"
            label="Config public time">
            <div v-if="appStatus.mails.length" class="row q-gutter-sm wrap q-pa-md">
              <q-date class="col" v-model="appStatus.publicTime" mask="YYYY/MM/DD HH:mm:ss" :options="dateLimit"
                color="green-7" style="min-width: 200px;" />
              <q-time class="col" v-model="appStatus.publicTime" mask="YYYY/MM/DD HH:mm:ss" :options="timeLimit"
                color="amber-9" style="min-width: 200px;" :default-date="appStatus.defaultPublicTime.split(' ')[0]"
                format24h with-seconds />
            </div>
          </q-expansion-item>

          <q-expansion-item expand-separator group="cfg" class="text-h6" icon="fa-solid fa-tags"
            label="Map column to mail field">
            <div class="q-pa-md">
              <q-select class="text-subtitle1" filled v-for="field, i in Object.keys(appStatus.field2ColIndex)" :key="i"
                v-model="appStatus.field2ColIndex[field]" :bg-color="`light-blue-${i + 1}`" :options="colOptions"
                map-options emit-value square clearable>
                <template v-slot:prepend>
                  <div class="text-h6 text-weight-bold">{{ `${field} : ` }}</div>
                </template>
              </q-select>
            </div>
          </q-expansion-item>
        </q-list>
      </q-scroll-area>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn-group glossy push class="q-mr-sm">
        <q-btn size="lg" color="indigo-8" icon="fa-solid fa-file-export" @click="exportTable"
          :disable="appStatus.mailFile === null" title="Export csv file" />
        <q-btn size="lg" color="indigo-8" icon="fa-solid fa-trash-can" @click="clearTable"
          :disable="appStatus.mailFile === null" title="Clear content" />
        <q-btn size="lg" color="red-8" icon="fa-solid fa-power-off" @click="reqTurnOff = true"
          :disable="appStatus.isProcessing" title="Shut down" />
      </q-btn-group>
    </q-card-actions>
  </q-card>

  <q-dialog v-model="reqTurnOff" persistent>
    <q-card>
      <q-card-section class="row items-center text-h6 text-red">
        <q-icon name="fa-solid fa-circle-exclamation" color="red" text-color="white" />
        <span class="q-ml-sm">Are you sure to shut down the app?</span>
      </q-card-section>

      <q-card-actions align="center">
        <q-btn flat label="Yes" color="red" v-close-popup no-caps @click="shutDownApp" />
        <q-btn flat label="No" color="grey" v-close-popup no-caps />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <table-col-handler @update-col-options="updateColOptions" />
  <table-row-handler />
</template>``

<script setup>
import { computed, ref, watch } from 'vue';
import { useQuasar, exportFile } from 'quasar';
import { useAppStatusStore } from 'src/stores/appStatus';
import papa from 'papaparse';
import axios from 'axios';
import dayjs from 'dayjs';
import TableColHandler from './TableColHandler.vue';
import TableRowHandler from './TableRowHandler.vue';

const $q = useQuasar();
const appStatus = useAppStatusStore();

const cols = computed(() => Object.keys(appStatus.mails[0] || {}).filter((e) => e !== 'Index'));
const colOptions = ref([]);
const newValueInCol = ref({});
const defaultPT = computed(() => (
  appStatus.defaultPublicTime === ''
    ? {} : {
      date: dayjs(appStatus.defaultPublicTime).format('YYYY/MM/DD'),
      ...dayjs(appStatus.defaultPublicTime).format('HH:mm:ss').split(':').reduce((obj, t, i) => {
        const timeStr = ['hr', 'min', 'sec'];
        obj[timeStr[i]] = Number(t);
        return obj;
      }, {}),
    }
));
const timeCfg = ref(null);
const reqTurnOff = ref(false);

function batchModCont(col, newVal) {
  appStatus.selectedRows.forEach((row) => {
    appStatus.mails[Number(row.Index) - 1][col] = newVal;
  });
}

function dateLimit(date) {
  return date >= defaultPT.value.date;
}

function timeLimit(hr, min, sec) {
  const [curCfgDate, curCfgTime] = appStatus.publicTime.split(' ');
  const [curCfgHour, curCfgMin] = curCfgTime.split(':');
  const inSameDate = curCfgDate === defaultPT.value.date;
  const inSameHour = Number(curCfgHour) === defaultPT.value.hr;
  const inSameMin = Number(curCfgMin) === defaultPT.value.min;

  if (inSameDate && hr < defaultPT.value.hr) return false;
  if (min && inSameDate && inSameHour && min < defaultPT.value.min) return false;
  if (sec && inSameDate && inSameHour && inSameMin && sec < defaultPT.value.sec) return false;
  return true;
}

function exportTable() {
  const isSuccess = exportFile(
    'New_mail_List.csv',
    papa.unparse(appStatus.mails.map((row) => {
      const extObj = { ...row };
      delete extObj.Index;
      return extObj;
    })),
    'text/csv',
  );

  if (!isSuccess) $q.notify({ message: 'Fail to export table' });
}

function clearTable() {
  appStatus.mailFile = null;
  appStatus.mails = [];
  appStatus.selectedRows = [];
  appStatus.defaultPublicTime = '';
  appStatus.publicTime = '';
}

async function shutDownApp() {
  try {
    await axios.post(`${appStatus.svrUrl}/exitSignal`);
    $q.notify({
      type: 'positive',
      icon: 'fa-solid fa-check',
      message: 'Shut down the app at 5 second',
    });
    setTimeout(() => window.close(), 5000);
  } catch (e) {
    console.error(e);
    $q.notify({ message: 'Fail to turn off the app.' });
  }
}

function switchSelectStatus(indexList) {
  if (colOptions.value.length) {
    indexList.forEach((index) => {
      if (colOptions.value[index]) colOptions.value[index].disable = !colOptions.value[index].disable;
    });
  }
}

function updateColOptions(index) {
  colOptions.value.splice(index, 1);
}

watch(cols, (v) => {
  colOptions.value = v.map((field, index) => ({
    label: field,
    value: index,
    disable: colOptions.value[index] ? colOptions.value[index].disable : false,
  }));
});

watch(colOptions, (newV, oldV) => {
  if (oldV.length) {
    if (!cols.value[appStatus.field2ColIndex.uid]) appStatus.field2ColIndex.uid = null;
    if (!cols.value[appStatus.field2ColIndex.title]) appStatus.field2ColIndex.title = null;
    if (!cols.value[appStatus.field2ColIndex.content]) appStatus.field2ColIndex.content = null;
  } else {
    appStatus.field2ColIndex.uid = newV.length >= 1 ? newV[0].value : null;
    appStatus.field2ColIndex.title = newV.length >= 2 ? newV[1].value : null;
    appStatus.field2ColIndex.content = newV.length >= 3 ? newV[2].value : null;
  }
});

watch(() => appStatus.field2ColIndex.uid, (newKey, oldKey) => {
  switchSelectStatus([oldKey, newKey]);
});

watch(() => appStatus.field2ColIndex.title, (newKey, oldKey) => {
  switchSelectStatus([oldKey, newKey]);
});

watch(() => appStatus.field2ColIndex.content, (newKey, oldKey) => {
  switchSelectStatus([oldKey, newKey]);
});

</script>
