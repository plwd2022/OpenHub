import os
import re
import sys

# Mapping of old support library packages to AndroidX packages
MAPPINGS = {
    # AppCompat
    "android.support.v7.app.AppCompatActivity": "androidx.appcompat.app.AppCompatActivity",
    "android.support.v7.app.ActionBar": "androidx.appcompat.app.ActionBar",
    "android.support.v7.app.AlertDialog": "androidx.appcompat.app.AlertDialog",
    "android.support.v7.app.AppCompatDelegate": "androidx.appcompat.app.AppCompatDelegate",
    "android.support.v7.widget.Toolbar": "androidx.appcompat.widget.Toolbar",
    "android.support.v7.widget.AppCompatTextView": "androidx.appcompat.widget.AppCompatTextView",
    "android.support.v7.widget.AppCompatImageView": "androidx.appcompat.widget.AppCompatImageView",
    "android.support.v7.widget.AppCompatButton": "androidx.appcompat.widget.AppCompatButton",
    "android.support.v7.widget.AppCompatEditText": "androidx.appcompat.widget.AppCompatEditText",
    "android.support.v7.widget.AppCompatCheckBox": "androidx.appcompat.widget.AppCompatCheckBox",
    "android.support.v7.widget.AppCompatRadioButton": "androidx.appcompat.widget.AppCompatRadioButton",
    "android.support.v7.widget.AppCompatSpinner": "androidx.appcompat.widget.AppCompatSpinner",
    "android.support.v7.widget.ActionMenuView": "androidx.appcompat.widget.ActionMenuView",
    "android.support.v7.widget.SwitchCompat": "androidx.appcompat.widget.SwitchCompat",
    "android.support.v7.widget.LinearLayoutCompat": "androidx.appcompat.widget.LinearLayoutCompat",
    "android.support.v7.widget.PopupMenu": "androidx.appcompat.widget.PopupMenu",
    "android.support.v7.view.ActionMode": "androidx.appcompat.view.ActionMode",
    "android.support.v7.content.res.AppCompatResources": "androidx.appcompat.content.res.AppCompatResources",

    # RecyclerView
    "android.support.v7.widget.RecyclerView": "androidx.recyclerview.widget.RecyclerView",
    "android.support.v7.widget.LinearLayoutManager": "androidx.recyclerview.widget.LinearLayoutManager",
    "android.support.v7.widget.GridLayoutManager": "androidx.recyclerview.widget.GridLayoutManager",
    "android.support.v7.widget.StaggeredGridLayoutManager": "androidx.recyclerview.widget.StaggeredGridLayoutManager",
    "android.support.v7.widget.DefaultItemAnimator": "androidx.recyclerview.widget.DefaultItemAnimator",
    "android.support.v7.widget.SimpleItemAnimator": "androidx.recyclerview.widget.SimpleItemAnimator",
    "android.support.v7.widget.helper.ItemTouchHelper": "androidx.recyclerview.widget.ItemTouchHelper",

    # CardView
    "android.support.v7.widget.CardView": "androidx.cardview.widget.CardView",

    # Design (Material)
    "android.support.design.widget.AppBarLayout": "com.google.android.material.appbar.AppBarLayout",
    "android.support.design.widget.CollapsingToolbarLayout": "com.google.android.material.appbar.CollapsingToolbarLayout",
    "android.support.design.widget.CoordinatorLayout": "androidx.coordinatorlayout.widget.CoordinatorLayout",
    "android.support.design.widget.FloatingActionButton": "com.google.android.material.floatingactionbutton.FloatingActionButton",
    "android.support.design.widget.NavigationView": "com.google.android.material.navigation.NavigationView",
    "android.support.design.widget.Snackbar": "com.google.android.material.snackbar.Snackbar",
    "android.support.design.widget.TabLayout": "com.google.android.material.tabs.TabLayout",
    "android.support.design.widget.TextInputLayout": "com.google.android.material.textfield.TextInputLayout",
    "android.support.design.widget.TextInputEditText": "com.google.android.material.textfield.TextInputEditText",
    "android.support.design.widget.BottomSheetDialog": "com.google.android.material.bottomsheet.BottomSheetDialog",
    "android.support.design.widget.BottomSheetBehavior": "com.google.android.material.bottomsheet.BottomSheetBehavior",
    "android.support.design.widget.BottomSheetDialogFragment": "com.google.android.material.bottomsheet.BottomSheetDialogFragment",

    # Fragment
    "android.support.v4.app.Fragment": "androidx.fragment.app.Fragment",
    "android.support.v4.app.FragmentManager": "androidx.fragment.app.FragmentManager",
    "android.support.v4.app.FragmentTransaction": "androidx.fragment.app.FragmentTransaction",
    "android.support.v4.app.FragmentPagerAdapter": "androidx.fragment.app.FragmentPagerAdapter",
    "android.support.v4.app.FragmentStatePagerAdapter": "androidx.fragment.app.FragmentStatePagerAdapter",
    "android.support.v4.app.DialogFragment": "androidx.fragment.app.DialogFragment",
    "android.support.v4.app.ListFragment": "androidx.fragment.app.ListFragment",
    "android.support.v4.app.LoaderManager": "androidx.loader.app.LoaderManager",

    # Support V4
    "android.support.v4.content.ContextCompat": "androidx.core.content.ContextCompat",
    "android.support.v4.content.FileProvider": "androidx.core.content.FileProvider",
    "android.support.v4.content.LocalBroadcastManager": "androidx.localbroadcastmanager.content.LocalBroadcastManager",
    "android.support.v4.content.Loader": "androidx.loader.content.Loader",
    "android.support.v4.content.AsyncTaskLoader": "androidx.loader.content.AsyncTaskLoader",
    "android.support.v4.view.ViewPager": "androidx.viewpager.widget.ViewPager",
    "android.support.v4.view.PagerAdapter": "androidx.viewpager.widget.PagerAdapter",
    "android.support.v4.view.GravityCompat": "androidx.core.view.GravityCompat",
    "android.support.v4.view.ViewCompat": "androidx.core.view.ViewCompat",
    "android.support.v4.view.WindowInsetsCompat": "androidx.core.view.WindowInsetsCompat",
    "android.support.v4.view.ActionProvider": "androidx.core.view.ActionProvider",
    "android.support.v4.view.MenuItemCompat": "androidx.core.view.MenuItemCompat",
    "android.support.v4.widget.DrawerLayout": "androidx.drawerlayout.widget.DrawerLayout",
    "android.support.v4.widget.SwipeRefreshLayout": "androidx.swiperefreshlayout.widget.SwipeRefreshLayout",
    "android.support.v4.widget.NestedScrollView": "androidx.core.widget.NestedScrollView",
    "android.support.v4.util.Pair": "androidx.core.util.Pair",
    "android.support.v4.util.ArrayMap": "androidx.collection.ArrayMap",
    "android.support.v4.util.SparseArrayCompat": "androidx.collection.SparseArrayCompat",

    # Annotations
    "android.support.annotation.NonNull": "androidx.annotation.NonNull",
    "android.support.annotation.Nullable": "androidx.annotation.Nullable",
    "android.support.annotation.IdRes": "androidx.annotation.IdRes",
    "android.support.annotation.StringRes": "androidx.annotation.StringRes",
    "android.support.annotation.LayoutRes": "androidx.annotation.LayoutRes",
    "android.support.annotation.ColorRes": "androidx.annotation.ColorRes",
    "android.support.annotation.DrawableRes": "androidx.annotation.DrawableRes",
    "android.support.annotation.StyleRes": "androidx.annotation.StyleRes",
    "android.support.annotation.CheckResult": "androidx.annotation.CheckResult",
    "android.support.annotation.CallSuper": "androidx.annotation.CallSuper",
    "android.support.annotation.IntDef": "androidx.annotation.IntDef",
    "android.support.annotation.UiThread": "androidx.annotation.UiThread",
    "android.support.annotation.WorkerThread": "androidx.annotation.WorkerThread",
    "android.support.annotation.RequiresApi": "androidx.annotation.RequiresApi",
    "android.support.annotation.Keep": "androidx.annotation.Keep",

    # Transition
    "android.support.transition.TransitionManager": "androidx.transition.TransitionManager",
    "android.support.transition.AutoTransition": "androidx.transition.AutoTransition",

    # VectorDrawable
    "android.support.graphics.drawable.VectorDrawableCompat": "androidx.vectordrawable.graphics.drawable.VectorDrawableCompat",
    "android.support.graphics.drawable.AnimatedVectorDrawableCompat": "androidx.vectordrawable.graphics.drawable.AnimatedVectorDrawableCompat",

    # Preference
    "android.support.v7.preference.Preference": "androidx.preference.Preference",
    "android.support.v7.preference.PreferenceFragmentCompat": "androidx.preference.PreferenceFragmentCompat",
    "android.support.v7.preference.PreferenceScreen": "androidx.preference.PreferenceScreen",
    "android.support.v7.preference.ListPreference": "androidx.preference.ListPreference",
    "android.support.v7.preference.CheckBoxPreference": "androidx.preference.CheckBoxPreference",
    "android.support.v7.preference.SwitchPreferenceCompat": "androidx.preference.SwitchPreferenceCompat",

    # Custom Tabs
    "android.support.customtabs": "androidx.browser.customtabs",

    # Constraint Layout
    "android.support.constraint.ConstraintLayout": "androidx.constraintlayout.widget.ConstraintLayout",

    # Palette
    "android.support.v7.graphics.Palette": "androidx.palette.graphics.Palette",
}

def migrate_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping binary file: {filepath}")
        return

    original_content = content

    # Replace simple strings first (for imports)
    for old, new in MAPPINGS.items():
        content = content.replace(old, new)

    # Some fuzzy replacements for wildcards or non-explicit imports
    # Replace package prefixes in XML files
    if filepath.endswith(".xml"):
        content = content.replace("android.support.v7.widget.Toolbar", "androidx.appcompat.widget.Toolbar")
        content = content.replace("android.support.v7.widget.RecyclerView", "androidx.recyclerview.widget.RecyclerView")
        content = content.replace("android.support.v4.widget.DrawerLayout", "androidx.drawerlayout.widget.DrawerLayout")
        content = content.replace("android.support.v4.widget.SwipeRefreshLayout", "androidx.swiperefreshlayout.widget.SwipeRefreshLayout")
        content = content.replace("android.support.v4.widget.NestedScrollView", "androidx.core.widget.NestedScrollView")
        content = content.replace("android.support.design.widget.CoordinatorLayout", "androidx.coordinatorlayout.widget.CoordinatorLayout")
        content = content.replace("android.support.design.widget.AppBarLayout", "com.google.android.material.appbar.AppBarLayout")
        content = content.replace("android.support.design.widget.CollapsingToolbarLayout", "com.google.android.material.appbar.CollapsingToolbarLayout")
        content = content.replace("android.support.design.widget.FloatingActionButton", "com.google.android.material.floatingactionbutton.FloatingActionButton")
        content = content.replace("android.support.design.widget.NavigationView", "com.google.android.material.navigation.NavigationView")
        content = content.replace("android.support.design.widget.TabLayout", "com.google.android.material.tabs.TabLayout")
        content = content.replace("android.support.design.widget.TextInputLayout", "com.google.android.material.textfield.TextInputLayout")
        content = content.replace("android.support.design.widget.TextInputEditText", "com.google.android.material.textfield.TextInputEditText")
        content = content.replace("android.support.v7.widget.CardView", "androidx.cardview.widget.CardView")
        content = content.replace("android.support.constraint.ConstraintLayout", "androidx.constraintlayout.widget.ConstraintLayout")

        # Behavior
        content = content.replace("android.support.design.widget.AppBarLayout$ScrollingViewBehavior", "com.google.android.material.appbar.AppBarLayout$ScrollingViewBehavior")

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Migrated: {filepath}")

def process_directory(root_dir, mode):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if mode == 'xml' and file.endswith(".xml"):
                migrate_file(filepath)
            elif mode == 'java1' and file.endswith(".java") and file[0].lower() < 'm':
                migrate_file(filepath)
            elif mode == 'java2' and file.endswith(".java") and file[0].lower() >= 'm':
                migrate_file(filepath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 migrate_androidx.py [xml|java1|java2]")
        sys.exit(1)

    process_directory(".", sys.argv[1])
