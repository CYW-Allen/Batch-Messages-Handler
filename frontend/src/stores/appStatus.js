import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStatusStore = defineStore('AppStatus', () => {
  const svrUrl = `http://${window.location.host}`;

  const mailFile = ref(null);
  const mails = ref([]);
  const mailTableRef = ref(null);

  const field2ColIndex = ref({
    uid: null,
    title: null,
    content: null,
  });
  const selectedRows = ref([]);

  const isProcessing = ref(false);

  const defaultPublicTime = ref('');
  const publicTime = ref('');
  const displayModifyColDlg = ref(false);
  const displayModifyRowDlg = ref(false);
  const rowModifyType = ref('add');

  return {
    svrUrl,
    mailFile,
    mails,
    mailTableRef,
    field2ColIndex,
    selectedRows,
    isProcessing,
    defaultPublicTime,
    publicTime,
    displayModifyColDlg,
    displayModifyRowDlg,
    rowModifyType,
  };
});
