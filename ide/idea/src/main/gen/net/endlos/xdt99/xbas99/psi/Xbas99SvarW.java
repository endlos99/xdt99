// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public interface Xbas99SvarW extends Xbas99NamedElement {

  @NotNull
  List<Xbas99FStr> getFStrList();

  @NotNull
  List<Xbas99Nexprn> getNexprnList();

  @NotNull
  List<Xbas99Sexpr> getSexprList();

  @NotNull
  List<Xbas99SvarR> getSvarRList();

  @NotNull String getName();

  PsiElement setName(String newName);

  PsiElement getNameIdentifier();

  ItemPresentation getPresentation();

  PsiReference getReference();

}
