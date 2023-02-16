# Plover Per-Application State
Plover plugin to make translation state function per application window and tab.

> **DISCLAIMER:** This plugin is still WIP and *will* cause Plover to function incorrectly under some circumstances.

## Installation
- Navigate to the installation directory for Plover and open a terminal / command prompt.

- > Run: `<exe_name> -s plover_plugins install -e plover-per-application-state`

    The [plover-application-controls](https://github.com/Pipatooa/plover-application-controls) plugin should be 
    installed automatically as a dependency.


- Restart Plover.

- Configure > Plugins > Enable both `application_controls` and `per_application_state`.

To disable the plugin at any point, disable `per_application_state`.

Disabling `application_controls` will prevent the plugin from being able to detect the currently active window.

## Important Dictionary Setup:

Any dictionary entries which result in a window being switched will need to be modified to include
`{PLOVER:per_application_state:prevent_merge}` at the start of the translation. This is to ensure that the plugin
correctly reloads state when the window is switched.

For example `{#Control(tab)}` will need to be modified to `{PLOVER:per_application_state:prevent_merge}{#Control(tab)}`.

This is NOT required for any `{PLOVER:application:}` commands from 
[plover-application-controls](https://github.com/Pipatooa/plover-application-controls).

## Commands:

The `{PLOVER:per_application_state}` command can be used to control state management. It takes a subcommand as its first 
argument, with further arguments separated by `:`.

For example, `{PLOVER:per_application_state:clear_all}` will clear all state.

| Window Command | Description                                                                               | Arguments | 
|----------------|-------------------------------------------------------------------------------------------|-----------|
| clear          | Clear the translation state for the current window tab                                    |           |
| clear_all      | Clears the current and stored translation states for all windows                          |           |
| clear_window   | Clears the current and stored translation states for the current active window            |           |
| prevent_merge  | Temporarily prevents state from being merged when a title changes as a result of a stroke |           |