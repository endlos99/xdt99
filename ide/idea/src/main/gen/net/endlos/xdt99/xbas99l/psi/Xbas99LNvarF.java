// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public interface Xbas99LNvarF extends Xbas99LNamedElement {

  @NotNull
  List<Xbas99LNvarW> getNvarWList();

  @NotNull
  List<Xbas99LSvarW> getSvarWList();

  @NotNull String getName();

  PsiElement setName(String newName);

  PsiElement getNameIdentifier();

  ItemPresentation getPresentation();

  PsiReference getReference();

}
