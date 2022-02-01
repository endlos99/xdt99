// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99.psi.Xbas99Types.*;
import net.endlos.xdt99.xbas99.psi.*;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public class Xbas99SvarFImpl extends Xbas99NamedElementImpl implements Xbas99SvarF {

  public Xbas99SvarFImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99Visitor visitor) {
    visitor.visitSvarF(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99Visitor) accept((Xbas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xbas99NvarW> getNvarWList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99NvarW.class);
  }

  @Override
  @NotNull
  public List<Xbas99SvarW> getSvarWList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99SvarW.class);
  }

  @Override
  public @NotNull String getName() {
    return Xbas99PsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xbas99PsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xbas99PsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xbas99PsiImplUtil.getPresentation(this);
  }

  @Override
  public PsiReference getReference() {
    return Xbas99PsiImplUtil.getReference(this);
  }

}
