<template>
  <s-btn-icon
    v-if="props.comments.length > 0"
    @click="emit('comment', {type: 'select', comment: props.comments[0], openSidebar: true})"
  >
    <v-badge 
      :content="props.comments.length" 
      floating 
      :max="9"
      :offset-x="6"
      :offset-y="6"
    >
      <v-icon icon="mdi-comment-text-outline" />
    </v-badge>
  </s-btn-icon>
  <s-btn-icon
    v-else
    @click="emit('comment', {type: 'create', comment: { collabPath: props.collabPath}})"
    :disabled="props.disabled"
    icon="mdi-comment-plus-outline"
    :style="{ opacity: props.isHovering ? 1 : 0 }"
  />
</template>

<script setup lang="ts">
import type { Comment } from '#imports';

const props = defineProps<{
  comments: Comment[];
  collabPath: string,
  disabled?: boolean;
  isHovering?: boolean|null;
}>();
const emit = defineEmits<{
  'comment': [value: any];
}>();
</script>
