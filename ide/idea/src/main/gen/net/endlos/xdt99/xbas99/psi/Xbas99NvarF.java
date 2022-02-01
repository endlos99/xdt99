// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public interface Xbas99NvarF extends Xbas99NamedElement {

  @NotNull
  List<Xbas99NvarW> getNvarWList();

  @NotNull
  List<Xbas99SvarW> getSvarWList();

  @NotNull String getName();

  PsiElement setName(String newName);

  PsiElement getNameIdentifier();

  ItemPresentation getPresentation();

  PsiReference getReference();

}
