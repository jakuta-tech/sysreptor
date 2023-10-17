<template>
  <s-autocomplete
    :model-value="props.modelValue"
    @update:model-value="emit('update:modelValue', $event)"
    :label="props.label"
    :items="allItems"
    :item-title="formatItemText"
    item-value="id"
    :return-object="props.returnObject"
    :rules="rules"
    :clearable="!props.required"
    :hide-no-data="false"
  >
    <template #append-item v-if="allItems.length > 0">
      <page-loader :items="items" />
    </template>
    <template #no-data v-if="allItems.length === 0 && items.hasNextPage.value">
      <page-loader :items="items" />
    </template>
    <template #append v-if="appendLink">
      <s-btn
        :to="`/designs/${returnObject ? props.modelValue?.id : props.modelValue}/pdfdesigner/`"
        target="_blank"
        :disabled="!props.modelValue"
        icon
        variant="text"
        class="mr-2"
      >
        <v-icon icon="mdi-chevron-right-circle-outline" />
        <s-tooltip activator="parent" text="Open Design" />
      </s-btn>
    </template>
    <template #message="messageProps" v-if="$slots.message"><slot name="message" v-bind="messageProps" /></template>
  </s-autocomplete>
</template>

<script setup lang="ts">
import isObject from "lodash/isObject";
import { ProjectType, ProjectTypeScope } from "~/utils/types";

const props = withDefaults(defineProps<{
  modelValue: ProjectType|string|null,
  returnObject?: boolean,
  required?: boolean,
  additionalItems?: ProjectType[],
  queryFilters?: Object,
  appendLink?: boolean,
  label?: string,
}>(), {
  returnObject: false,
  required: false,
  additionalItems: () => [],
  queryFilters: () => ({}),
  appendLink: false,
  label: 'Design',
});
const emit = defineEmits<{
  (e: 'update:modelValue', value: ProjectType|string|null): void,
}>();

const items = useSearchableCursorPaginationFetcher<ProjectType>({
  baseURL: '/api/v1/projecttypes/',
  query: {
    ordering: 'name',
    scope: ['global', 'private'],
    ...props.queryFilters
  }
});

const rules = [
  (v: any) => !props.required || Boolean(v) || 'Item is required',
]

const projectTypeStore = useProjectTypeStore();
const initialProjectType = ref<ProjectType|null>(null);
useLazyAsyncData(async () => {
  if (props.modelValue && !props.additionalItems.some(pt => [props.modelValue, (props.modelValue as any)?.id].includes(pt.id))) {
    if (isObject(props.modelValue)) {
      initialProjectType.value = props.modelValue;
    } else {
      initialProjectType.value = await projectTypeStore.getById(props.modelValue as string);
      if (props.returnObject) {
        emit('update:modelValue', initialProjectType.value);
      }
    }
  }
});

const allItems = computed(() => {
  return props.additionalItems.concat(items.data.value).concat(initialProjectType.value ? [initialProjectType.value] : []);
})

function formatItemText(pt: ProjectType) {
  return pt.name + ({
    [SourceEnum.IMPORTED]: ' (imported)',
    [SourceEnum.CUSTOMIZED]: ' (customized)',
    [SourceEnum.SNAPSHOT]: ` (from ${pt?.created?.split('T')?.[0]})`,
  }[pt?.source as string] || '') +
      (pt?.scope === ProjectTypeScope.PRIVATE ? ' (private design)' : '');
}
</script>