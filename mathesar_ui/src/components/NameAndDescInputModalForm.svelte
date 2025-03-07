<script lang="ts">
  /**
   * This component is currently used for objects where name and description
   * need to be entered by the user. This is used in places such as:
   * - Adding/Editing schema
   * - Saving Exploration
   *
   * A more common modal-form component can be created by utilizing FormBuilder
   * if such a need arises in the future.
   */
  import { tick } from 'svelte';
  import { _ } from 'svelte-i18n';

  import TextArea from '@mathesar/component-library/text-area/TextArea.svelte';
  import { toast } from '@mathesar/stores/toast';
  import {
    CancelOrProceedButtonPair,
    ControlledModal,
    LabeledInput,
    type ModalController,
    TextInput,
  } from '@mathesar-component-library';

  export let saveButtonLabel = $_('save');
  export let controller: ModalController;
  export let getNameValidationErrors: (name: string) => string[];
  export let getInitialName: () => string = () => '';
  export let getInitialDescription: () => string = () => '';
  export let save: (name: string, description: string) => Promise<void>;
  export let namePlaceholder = $_('name');
  export let descriptionPlaceholder = $_('description');
  export let disabled = false;

  let isSubmitting = false;
  let inputElement: HTMLInputElement;
  let initialName = '';
  let name = '';
  let description = '';
  let nameHasChanged = false;

  async function init() {
    initialName = getInitialName();
    name = initialName;
    description = getInitialDescription();
    nameHasChanged = false;
    if (!inputElement) {
      return;
    }
    await tick();
    inputElement.focus();
    inputElement.setSelectionRange(0, inputElement.value.length);
  }

  async function handleSave() {
    try {
      isSubmitting = true;
      await save(name, description);
      controller.close();
    } catch (error) {
      toast.fromError(error);
    } finally {
      isSubmitting = false;
    }
  }

  $: nameValidationErrors = getNameValidationErrors(name);
  $: canProceed = !nameValidationErrors.length && !disabled;
</script>

<ControlledModal
  {controller}
  allowClose={!isSubmitting}
  on:open={init}
  closeOn={['button', 'esc', 'overlay']}
>
  <slot slot="title" name="title" {initialName} />

  <div class="form-container">
    <slot name="helpText" />

    <div class="input-container">
      <LabeledInput label={$_('name')} layout="stacked">
        <TextInput
          bind:value={name}
          bind:element={inputElement}
          aria-label={$_('name')}
          on:input={() => {
            nameHasChanged = true;
          }}
          disabled={isSubmitting || disabled}
          placeholder={namePlaceholder}
          id="name"
        />
        {#if nameHasChanged && nameValidationErrors.length}
          <p class="error">
            {nameValidationErrors.join(' ')}
          </p>
        {/if}
      </LabeledInput>
    </div>

    <div class="input-container">
      <LabeledInput label={$_('description')} layout="stacked">
        <TextArea
          bind:value={description}
          aria-label={$_('description')}
          disabled={isSubmitting || disabled}
          placeholder={descriptionPlaceholder}
        />
      </LabeledInput>
    </div>
  </div>
  <CancelOrProceedButtonPair
    proceedButton={{ label: saveButtonLabel }}
    onCancel={() => {
      controller.close();
    }}
    onProceed={handleSave}
    {canProceed}
    slot="footer"
  />
</ControlledModal>

<style lang="scss">
  .error {
    color: var(--color-error);
    font-size: 0.8rem;
  }

  .form-container {
    display: flex;
    flex-direction: column;

    > :global(* + *) {
      margin-top: 0.25rem;
    }
  }

  .form-container > .input-container {
    margin-bottom: 1rem;
  }

  .input-container {
    display: flex;
    flex-direction: column;
  }

  .input-container > .error {
    margin-top: 0.25rem;
  }
</style>
