<template>
  <q-page :style-fn="tweakPageH" class="q-pa-lg bg-light-blue-1">
    <div class="fit column ">
      <div class="col-10 row q-pa-sm">
        <div class="col-8 full-height q-mr-md">
          <data-field />
        </div>
        <div class="col full-height">
          <operation-field />
        </div>
      </div>
      <div class="col-2 q-pa-sm">
        <div class="fit" style="border: 1px solid purple;">Request handler field</div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import DataField from 'src/components/DataField.vue';
import OperationField from 'src/components/OperationField.vue';

function tweakPageH(offset) {
  return { height: offset ? `calc(100vh - ${offset}px)` : '100vh' };
}

</script>
